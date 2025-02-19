1. write a prompt for the data mapper ai and paste it in the prompt_store/mapping_prompt.txt file. 
2. run the run.py file to see the output. 

# ai-flask-app
# To Run the flask app
cd data-mapper-ai
python -m flask run 

Follow the link http://127.0.0.1:5000

## Testing the Email API with Postman

### Endpoint Details
- **URL**: `http://127.0.0.1:5000/api/carrier/send-email`
- **Method**: POST
- **Content-Type**: application/json

### Request Body
```json
{
    "carrier_name": "Data Mapper AI Test 2"
}
```
