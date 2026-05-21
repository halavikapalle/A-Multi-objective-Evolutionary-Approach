\# A Multi-Objective Evolutionary Approach (MOEAD)



\## Overview



This project implements a Multi-Objective Evolutionary Algorithm based on Decomposition (MOEA/D) with a web-based dashboard for managing optimization experiments and viewing results.



The application allows users to:



\- Run multi-objective optimization processes

\- Store optimization history in a database

\- Visualize experiment information through a web interface

\- Track generated solutions and performance metrics



\## Features



\- Multi-Objective Evolutionary Algorithm (MOEA/D)

\- Interactive web dashboard

\- Optimization history management

\- SQLite database integration

\- Python-based implementation

\- Simple and lightweight architecture



\## Project Structure



```text

MOEAD/

│

├── app.py

├── moead\_engine.py

├── requirements.txt

├── templates/

│   └── dashboard.html

├── mec\_history.db

└── README.md

```



\## Technologies Used



\- Python

\- Flask

\- SQLite

\- HTML

\- CSS

\- JavaScript



\## Installation



\### Clone Repository



```bash

git clone https://github.com/halavikapalle/A-Multi-objective-Evolutionary-Approach.git

```



\### Navigate to Project Directory



```bash

cd A-Multi-objective-Evolutionary-Approach

```



\### Create Virtual Environment



```bash

python -m venv venv

```



\### Activate Virtual Environment



Windows:



```bash

venv\\Scripts\\activate

```



Linux/Mac:



```bash

source venv/bin/activate

```



\### Install Dependencies



```bash

pip install -r requirements.txt

```



\## Run Application



```bash

python app.py

```



The application will start locally and can be accessed through your browser.



\## Usage



1\. Launch the application.

2\. Open the dashboard.

3\. Configure optimization parameters.

4\. Execute the MOEA/D algorithm.

5\. Analyze generated solutions and optimization results.



\## Future Enhancements



\- Advanced visualization of Pareto fronts

\- Export optimization results

\- User authentication

\- Real-time optimization monitoring

\- Cloud deployment support



\## Author



\*\*Halavika Palle\*\*



GitHub: https://github.com/halavikapalle



