<a name="readme-top"></a>


<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">MassEmailSender</h3>

  <p align="center">
    Tested with Gmail
  </p>
</div>

<!-- ABOUT THE PROJECT -->
# Prerequisites

`python3`
## Installation

1. Clone the repo
   ```sh
   git clone https://github.com/sinmentis/MassEmailSender
   ```
2. Configure Json files, follow the format with provided  files
3. Send Emails!
   ```sh
   cd src && python3 main.py
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Configuration
Check `src/config_json` folder for example files.
Notes `pyhunter_API.txt` is needed if wants to use hunter.io for email collection. Free account can add up to 10 emails if that helps :)

## Pyinstaller
1. A nice easy pyinstaller spec file iss provided for executable generation
```sh
cd src && pyinstaller --noconfirm main.spec
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

# Introduction

1. The UI is based on PySide6, mostly draw in QML
2. The Backend is written in python.
3. Email parser are open to be improved, currently using following, huge thanks to open source!
   1. [EmailAll](https://github.com/Taonn/EmailAll)
   2. [Frisbee](https://github.com/9b/frisbee)
   3. [PyHunter](https://github.com/VonStruddle/PyHunter)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
# Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
