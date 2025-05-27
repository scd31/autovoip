import os
import time

import pjsua2 as pj
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_env_var(name):
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Required environment variable '{name}' is not set")
    return value


# SIP configuration from environment variables
SIP_IP = get_env_var("SIP_IP")
SIP_PORT = int(get_env_var("SIP_PORT"))
SIP_USERNAME = get_env_var("SIP_USERNAME")
SIP_PASSWORD = get_env_var("SIP_PASSWORD")


# Subclass to extend the Account and get notifications etc.
class Account(pj.Account):
    def __init__(self):
        pj.Account.__init__(self)
        self.call = None

    def onRegState(self, prm):
        print(f"*** Registration state: {prm.reason}")

    def onIncomingCall(self, prm):
        call = pj.Call(self, prm.callId)
        self.call = call

        ci = call.getInfo()
        print(f"*** Incoming call from: {ci.remoteUri}")

        call_prm = pj.CallOpParam()
        call_prm.statusCode = 200  # OK
        call.answer(call_prm)


# Call class to handle call events
class Call(pj.Call):
    def __init__(self, acc, call_id=pj.PJSUA_INVALID_ID):
        pj.Call.__init__(self, acc, call_id)

    def onCallState(self, prm):
        ci = self.getInfo()
        print(f"*** Call state: {ci.stateText}")

    def onCallMediaState(self, prm):
        ci = self.getInfo()
        print(f"*** Call media state: {ci.mediaStateText}")


def sip_client():
    # Create and initialize the library
    ep_cfg = pj.EpConfig()
    ep = pj.Endpoint()
    ep.libCreate()
    ep.libInit(ep_cfg)

    # Create SIP transport
    sip_tp_config = pj.TransportConfig()
    sip_tp_config.port = 0  # Let system choose available port
    ep.transportCreate(pj.PJSIP_TRANSPORT_UDP, sip_tp_config)

    # Start the library
    ep.libStart()

    # Configure account
    acc_cfg = pj.AccountConfig()
    acc_cfg.idUri = f"sip:{SIP_USERNAME}@{SIP_IP}:{SIP_PORT}"
    acc_cfg.regConfig.registrarUri = f"sip:{SIP_IP}:{SIP_PORT}"

    # Add credentials
    cred = pj.AuthCredInfo("digest", "*", SIP_USERNAME, 0, SIP_PASSWORD)
    acc_cfg.sipConfig.authCreds.append(cred)

    # Create the account
    acc = Account()
    acc.create(acc_cfg)

    print(f"Registered as {SIP_USERNAME}@{SIP_IP}:{SIP_PORT}")
    print("Waiting for calls or press Enter to make a call...")

    # Wait for user input or incoming call
    user_input = input("Enter a number to call or press Enter to wait: ")

    if user_input:
        # Make outgoing call
        call_prm = pj.CallOpParam(True)
        call = Call(acc)
        call.makeCall(f"sip:{user_input}@{SIP_IP}:{SIP_PORT}", call_prm)

        print(f"Call initiated to {user_input}")
        print("Call will automatically end in 30 seconds...")
        time.sleep(30)

        # Hangup
        if call:
            call_prm = pj.CallOpParam()
            call_prm.statusCode = 200
            call.hangup(call_prm)
    else:
        # Just wait for incoming calls
        print("Waiting for incoming calls (60 seconds)...")
        time.sleep(60)

    # Cleanup
    print("Shutting down...")
    ep.libDestroy()


# Main entry point
if __name__ == "__main__":
    try:
        sip_client()
    except Exception as e:
        print(f"Error: {e}")
