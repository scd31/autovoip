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
            pjsua2
            black
            flake8
            isort
            python-dotenv
          ]
        );
      in
      {
        devShells = {
          default = pkgs.mkShell {
            packages = [
              pkgs.pyright
              python
            ];
          };
        };
      }
    );
}
