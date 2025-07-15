import anthropic
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import boto3
import uuid

api_key=""

client=anthropic.Anthropic(api_key=api_key)


answer=client.messages.create(
        model="claude-3-5-haiku-20241022",
        temperature=1,
        max_tokens=100,
        system="I need a helpful, authentic answer to this question that real people would find valuable. Write in a conversational tone like you're genuinely helping someone who asked this question. Focus on being practical and honest rather than overly polished.",
        messages=[{
         "role":"user",
         "content":[{
           "type":"text",
           "text":"Tell me about Yuvraj Singh"
              }]}])

print(answer.content[0].text)


driver=webdriver.Firefox()
driver.maximize_window()
driver.get("https://quillbot.com/paraphrasing-tool")

time.sleep(5)


driver.find_element(By.ID,'paraphraser-input-box').send_keys(answer.content[0].text)
time.sleep(2)
driver.find_element(By.XPATH,"/html/body/div[1]/div/div[3]/section[1]/div/div/div/section/div[2]/div/div/div[3]/div[1]/div[2]/div/div[1]/div/div[2]/div/div[2]/span/div/button/span[1]").click()
time.sleep(10)
output_text=driver.find_element(By.ID,"paraphraser-output-box")
print(output_text)
output_text=output_text.text
print(output_text)
time.sleep(2)
driver.quit()

aws_access_key=""
aws_secret_key=""
s3=boto3.client('s3',aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key)
file_name=f"{uuid.uuid4()}.txt"
s3.put_object(Bucket="filesfortestingin",Key=file_name,Body=output_text)
