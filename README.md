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

    ```shell
    virtualenv .chikaraVenv
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

    ```shell
    pip install -r requirements.txt
    ```

5. Start the APIREST:

    ```shell
    uvicorn main:app --reload
    ```
