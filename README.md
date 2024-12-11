# Project Name
Program Backend API for Machine Learning Models.

## Description
This program uses the Flask Python framework which will provide herbal plant recommendations based on the symptoms requested and the prediction value of the Machine Learning Model.
Applications are deployed using Google Cloud Run through Google Cloud Build and Google Container Registry.

## Key Features
- Recommendation features
  
## Installation
Steps to install and run this project on local.
1. Clone this repository:
   ```bash
   git clone https://github.com/HerbaMate-Bangkit-Capstone/HerbaMate--Model---CC.git
   
2. Extract and go to the project folder:
   ```bash
   cd HerbaMate--Model---CC
   
3. Install dependencies:
   ```bash
   pip install -r requirements.txt

4. Run the project:
   ```bash
   python app.py
   
5. URL Project Localhost:
   ```bash
   http://localhost:5000/herb/predict
   
6. Make a request using Postman:
   - Post symptoms to get recommendations:
     - Request:
       ```bash
       {
           "symptoms": "Batuk,Sakit tenggorokan,Perut kembung,Mual"
       }
       
     - Response:
       ```bash
       {
          "code": 200,
          "message": "Successful herbs recommendations",
          "prediction score": 0.09604641795158386,
          "result data": [
              {
                  "herbs": "Adas",
                  "image_link": "image_link_herbals",
                  "latin_name": "(Foeniculum vulgare)",
                  "usage_method": "Rebus 1-2 sendok teh biji adas dalam 1,5 gelas air hingga tersisa sekitar satu gelas. Setelah mendidih, saring air rebusan dan minum selagi hangat. Air                                    rebusan ini dapat diminum 2-3 kali sehari untuk membantu meredakan batuk, karena adas memiliki sifat ekspektoran yang membantu mengencerkan lendir dan                                     melegakan saluran pernapasan."
               },
               {
                  "herbs": "Daun jintan",
                  "image_link": "image_link_herbals",
                  "latin_name": "(Coleus amboinicus)",
                  "usage_method": "Haluskan 5-7 lembar daun jintan dengan sedikit air, lalu peras dan ambil sarinya. Minum sari daun jintan ini sekali sehari untuk membantu meredakan                                        batuk, berkat sifat ekspektoran yang membantu mengencerkan lendir."
                }
            ]
        }

