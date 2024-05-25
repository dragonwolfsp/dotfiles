# installing

* ensure [chezmoi](https://github.com/twpayne/chezmoi) is installed.

<details>
<summary>Installing on windows:</summary>
1. scoop:
```console
$ scoop install chezmoi
```
2. choco:
```console
$ choco install chezmoi
```
3. winget:
```console
$ winget install twpayne.chezmoi
```
</details>

<details>
<summary>Installing on Mac Os:</summary>
1. homebrew:
```console
$ brew install chezmoi
```
2. macports:
```console
$ port install chezmoi
```
</details>

<details>
<summary>Installing on linux:</summary>
1. alpine:
```console
$ apk add chezmoi
 ```
 2. arch:
 ```console
$ pacman -S chezmoi
 ```
 3. nix os:
 ```console
$ nix-env -i chezmoi
 ```
 4. opensuse:
 ```console
$ zypper install chezmoi
```
5. termux:
```console
$ pkg install chezmoi
```
6. void linux:
```console
$ xbps-install -S chezmoi
```
7. ubuntu/snap:
```console
$ snap install chezmoi --classic
```
</details>

<details>
<summary>Installing on FreeBSD</summary>
1. pkg:
```
$ pkg install chezmoi
```
</details>

* chezmoi init https://github.com/blindelectron/dotfiles
* chezmoi apply