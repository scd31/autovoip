{
  description = "AutoVOIP";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {inherit system;};
      python = pkgs.python3.withPackages (ps:
        with ps; [
          black
          flake8
          isort
        ]);
    in {
      devShells = {
        default = pkgs.mkShell {
          packages = [
            pkgs.python312Packages.jupyterlab
            pkgs.python312Packages.jupyterlab-server
            pkgs.jupyter
            pkgs.pyright
            python
          ];
        };
      };
    });
}
