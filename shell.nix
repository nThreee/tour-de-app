{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    # nativeBuildInputs is usually what you want -- tools you need to run
    nativeBuildInputs = with pkgs.buildPackages; [
      (python3.withPackages (python-pkgs: with python-pkgs; [
        python-lsp-server
        flask
        flask-cors
        flask-sqlalchemy
        pymysql
        python-dotenv
      ]))
    ];
}
