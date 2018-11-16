# Heart Rate Sentinel Server

This project interacts with a database containing patient heart rate information. If a patient posts a tachycardic heart rate, the physician for the patient receives an email.

The program `heart_server.py` interacts with the database, and has functions to add patients, heart rates, and get average heart rates for patients.

To run the programs on the server, use `interact_with_server.py`. This program has the IP address for the server, as well as pre-formatted functions to do the git and post requests interpreted by the server.

The server can be reached at the following address: http://vcm-7302.vm.duke.edu
