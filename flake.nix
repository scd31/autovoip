{
  description = "AutoVOIP";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python3.withPackages (
          ps: with ps; [
            black
            flake8
            isort
          ]
        );
      in
      {
        devShells = {
          default = pkgs.mkShell {
            packages = [
              pkgs.pyright
              python
              pkgs.portaudio
            ];

            shellHook = ''
              if [ ! -e venv ]; then
                python -m venv venv
              fi
              source venv/bin/activate
              pip install -r requirements.txt
            '';
          };
        };
      }
    );
}
