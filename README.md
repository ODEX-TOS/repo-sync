[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url] [![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPL License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/ODEX-TOS/repo-sync">
    <img src="https://tos.odex.be/images/logo.svg" alt="Logo" width="150" height="150">
  </a>

  <h3 align="center">TOS repo manager</h3>

  <p align="center">
    A tool to `fork` the main repository
    <br />
    <br />
    <a href="https://wiki.odex.be">View wiki</a>
    ·
    <a href="https://github.com/ODEX-TOS/repo-sync/issues">Report Bug</a>
    ·
    <a href="https://github.com/ODEX-TOS/repo-sync/issues">Request Feature</a>
  </p>
</p>

<p align="center">
   <a href="https://www.paypal.com/donate?hosted_button_id=X892LWMTDU6D6">
     <img src="https://raw.githubusercontent.com/stefan-niedermann/paypal-donate-button/master/paypal-donate-button.png" alt="Donate with PayPal" width="300" height="100"/>
   </a>
</p>

<!-- TABLE OF CONTENTS -->

## Table of Contents

- [About the Project](#about-the-project)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Ring Levels](#ring-levels)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgements)

<!-- ABOUT THE PROJECT -->

## About The Project

### Built By

- [F0xedb](https://www.odex.be)

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

All that is needed is a working `python 3` installation to sync repository data

If you want to host your own repo, you will either need a working reverse proxy on the host or a working docker environment.


### Installation

1. Clone the repo

```sh
git clone https://github.com/ODEX-TOS/repo-sync.git
# or use the distributed script from the tos repo
tos -S repo-manager
```

2. deploy the repository
```sh
repo-manager deploy # interactively deploy the repo

# deploy the repository to a given path
repo-manager deploy --type host --path /path/to/webserver/root # this will sync the repository to a given path

# deploy the repository in docker, using nginx and give it a hostname to generate the given TLS certificates
repo-manager deploy --type docker --backend nginx --domain repo.example.com

# deploy using an external traefik instance (Only support traefik v2.x)
repo-manager deploy --type docker --backend treafik --domain repo.example.com --external-traefik name_of_traefik_network
```
> Note: Only run one of the above commands, they are for different deployment models, use the one that applies the most to you

3. Check that everything is working
```sh
repo-manager info
```

4. Optionally change the ring level
```sh
repo-manager sync --ring 2 # we treat this as a ring 2 repository
```

5. Periodically sync the repo
```sh
repo-manager systemctl # setup a daily sync timer to sync the repo
```

6. Make this repo official
```sh
# Create an issue in the tos repo github project, developers will review it and potentially make it an official repo
repo-manager commit
```

## Usage

Repo-manager is a tool to allow you to quickly deploy a TOS repo, and make it sync with upstream.

### Ring levels

It is important that you are aware of what ring levels are/mean when setting up a tos repo.

#### Ring level 1

This is the `root` level, this means that upstream tos builds packages and uploads them to this ring level.
In the case of tos this ring level contains one server with 1GB network bandwidth.
This server is purely to sync `ring level 2` servers and shouldn't be used directly by end users.

These are the url's of ring level 1 servers:

- [repo.odex.be](https://repo.odex.be) - The official server that should be used as ring-level 1
- [testing.odex.be](https://testing.odex.be) - The testing server which can contain an invalid state or buggy programs (Should not be used as upstream)

> Note: Nobody is allowed to be a `ring level 1` server, if you want to most privileges possible use a ring-level 2 server


#### Ring level 2

This is the ring level directly behind ring level 1, these are servers that should have the following requirements:

* Minimum of 1GB network speeds (Upload)
* Sync at least every 6 hours from a ring-level 1 server

These servers are allowed to be in the mirrorlist `/etc/pacman.d/tos-mirrorlist` and can be used to sync data for end users

#### Ring level 3

This is the ring level directly behind ring level 2, these are servers that should have the following requirements:

* Minimum of 100MB network speeds (Upload)
* Sync at least every day from a ring-level 2 server

These servers sync from a tier 2 ring, they are also allowed to be in the mirrorlist

<!-- ROADMAP -->

## Roadmap

See the
[open issues](https://github.com/ODEX-TOS/repo-sync/issues) for a
list of proposed features (and known issues).

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to
be learn, inspire, and create. Any contributions you make are **greatly
appreciated**. First ensure you have read the [wiki](https://wiki.odex.be)
especially the [style guide](https://wiki.odex.be/Developer/style-guide) page

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- CONTACT -->

## Contact

Tom Meyers - tom@odex.be

Project Link:
[https://github.com/ODEX-TOS/repo-sync](https://github.com/ODEX-TOS/repo-sync)

<!-- ACKNOWLEDGEMENTS -->

## Acknowledgments

- [F0xedb](https://www.odex.be)
- [TOS Homepage](https://tos.odex.be)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/ODEX-TOS/repo-sync.svg?style=flat-square
[contributors-url]: https://github.com/ODEX-TOS/repo-sync/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ODEX-TOS/repo-sync.svg?style=flat-square
[forks-url]: https://github.com/ODEX-TOS/repo-sync/network/members
[stars-shield]: https://img.shields.io/github/stars/ODEX-TOS/repo-sync.svg?style=flat-square
[stars-url]: https://github.com/ODEX-TOS/repo-sync/stargazers
[issues-shield]: https://img.shields.io/github/issues/ODEX-TOS/repo-sync.svg?style=flat-square
[issues-url]: https://github.com/ODEX-TOS/repo-sync/issues
[license-shield]: https://img.shields.io/github/license/ODEX-TOS/repo-sync.svg?style=flat-square
[license-url]: https://github.com/ODEX-TOS/repo-sync/blob/release/LICENSE
[product-screenshot]: https://tos.odex.be/images/logo.svg
