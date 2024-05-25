# installing

* ensure [chezmoi](https://github.com/twpayne/chezmoi) is installed.

<details>
<summery>Installing on windows:</summery>
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
<summery>Installing on Mac Os:</summery>
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
<summery>Installing on linux:</summery>
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
<summery>Installing on FreeBSD</summery>
1. pkg:
```
$ pkg install chezmoi
```
</details>

* chezmoi init https://github.com/blindelectron/dotfiles
* chezmoi apply