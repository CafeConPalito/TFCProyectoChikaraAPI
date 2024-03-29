# TFGProyectoChikaraAPI

## Getting Started

To get started with the TFGProyectoChikaraAPI project, follow these steps:

### Prerequisites

- Python 3.11.6
- virtualenv

### Installation

1. Clone the repository:

    ```shell
    git clone https://github.com/your-username/TFGProyectoChikaraAPI.git
    ```
2. Create a virtual environment:

    Windows
    ```shell
    virtualenv .chikaraVenv
    ```
   MacOs | Linux
   ```shell
    python3 -m venv .chikaraVenv
   ```
3. Activate the virtual environment(Windows):

    Windows
    ```shell
    .chikaraVenv/Scripts/activate
    ```
    
    MacOs | Linux

    ```shell
    .chikaraVenv/bin/activate
    ```

4. Install the required dependencies:

    Windows
    ```shell
    pip install -r requirements.txt
    ```
    MacOs | Linux

    ```shell
    pip3 install -r requirements.txt
    ```

5. Create a .env file in the root directory of the project and add the following parameters:

    ```
    DB_HOST=localhost
    DB_PORT=3306
    DB_NAME=chikara
    DB_USER={user}
    DB_PASSWORD={password}

    # Variables de mongodb
    DB_USER_MONGO = {user}
    DB_PASSWORD_MONGO= {password}
    DB_CLUSTER = {url}
    DB_NAME_MONGO = ChikaraDB
    DB_COLLECTION = chiks
    ```

6. Start the APIREST:

    ```shell
    uvicorn main:app --reload
    ```


