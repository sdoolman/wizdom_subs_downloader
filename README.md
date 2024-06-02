# Wizdom Subtitles Downloader

This project is a Python tool to download subtitles from [wizdom.xyz](https://wizdom.xyz). It supports TV show subtitles and uses several Python libraries for downloading and matching subtitles with TV show titles.

## Features

- Downloads subtitles from wizdom.xyz
- Matches TV show titles using IMDb
- User-friendly choice menu for selecting subtitles

## Libraries Used

- `aiohttp`: For asynchronous HTTP requests
- `requests`: For making HTTP requests
- `imdb`: For matching TV show titles
- `bullet`: For creating a choice menu

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/wizdom-subtitles-downloader.git
    cd wizdom-subtitles-downloader
    ```

2. Install `pipenv` if you haven't already:

    ```sh
    pip install pipenv
    ```

3. Install the required libraries:

    ```sh
    pipenv install
    ```

4. Activate the virtual environment:

    ```sh
    pipenv shell
    ```

## Usage

Run the script to start the subtitle downloader. The script expects three arguments: the output directory, the name of the TV show, and the name of the movie.

```sh
python main.py <output_directory> <tv_show_name> <season_number>
```

Follow the on-screen instructions to select and download the desired subtitles.

## Credits

This project is a Python reimplementation of the original JavaScript project by [maormagori](https://github.com/maormagori/wizdom-stremio-v2). Full credit goes to him for the original concept and implementation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```
