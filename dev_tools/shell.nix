let
  pkgs = import <nixpkgs> { };
  # define version
  using_python = (pkgs.enableDebugging pkgs.python312).overrideAttrs (
    oldAttrs: {
      keepDebugInfo = true;
    }
  );
  # import required python packages
  required_python_packages = import ./py_requirements.nix;
  #
  extra_search_directory = ".extra-stub-path";
  pyenv = using_python.withPackages required_python_packages;
in
pkgs.mkShell {
  packages = [
    pyenv
    pkgs.cmake
    pkgs.gdb
    pkgs.valgrind
    # pkgs.gcc
    pkgs.clang
    pkgs.gcc
  ];
  shellHook = ''
    if [[ ! -d ${extra_search_directory} ]]; then mkdir ${extra_search_directory}; fi
    ensure_symlink() {
        local link_path="$1"
        local target_path="$2"
        if [[ -L "$link_path" ]] && [[ "$(readlink "$link_path")" = "$target_path" ]]; then
            return 0
        fi
        rm -f "$link_path" > /dev/null 2>&1
        ln -s "$target_path" "$link_path"
    }

    for file in ${pyenv}/${using_python.sitePackages}/*; do
        ensure_symlink ${extra_search_directory}/$(basename $file) $file
    done
    for file in ${extra_search_directory}/*; do
        if [[ -L "$file" ]] && [[ "$(dirname $(readlink "$file"))" != "${pyenv}/${using_python.sitePackages}" ]]; then
            rm -f "$file"
        fi
    done
    ensure_symlink ${extra_search_directory}/python ${pyenv}/bin/python
    ensure_symlink ${extra_search_directory}/valgrind ${pkgs.valgrind}/bin/valgrind
    export CC=${pkgs.clang}/bin/clang
    export CXX=${pkgs.clang}/bin/clang++
    ensure_symlink ${extra_search_directory}/clang $CC
    ensure_symlink ${extra_search_directory}/clang++ $CXX
    export NIX_DEBUG_INFO_DIRS=/home/antares/Documents/GitHub/cpython-debug/Python-3.12.3/
  '';
}
