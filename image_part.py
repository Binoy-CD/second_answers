import requests
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import base64

def get_cd_imgae_details_stage(img_path):
    base_api = 'https://qacmsstage.collegedunia.com/'
    transport = AIOHTTPTransport(url = base_api, headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7Im1vYmlsZVZlcmlmaWVkIjpmYWxzZSwiX2lkIjoiNjIyNzVkYTEwMTVmM2MyNzVjNzE1YTM2Iiwicm9sZUlkIjoiNjIyMGI2Njk4YWU0Y2RhYjVkYmRlNzg4Iiwic3RhdHVzIjoiQUNUSVZFIiwibGFuZ3VhZ2UiOiJlbiIsImVtYWlsVmVyaWZpZWQiOnRydWUsIm1vYmlsZSI6Iis5MTkxNDA5NTYwOTciLCJlbWFpbCI6InByYWJhbC5ndXB0YUBjb2xsZWdlZHVuaWEuY29tIiwibGFzdE5hbWUiOiJHdXB0YSIsImZpcnN0TmFtZSI6IlByYWJhbCIsImV4YW1QcmVmZXJlbmNlcyI6W10sIm5hbWUiOiJQcmFiYWwgR3VwdGEiLCJjcmVhdGVkQXQiOiIyMDIyLTAzLTA4VDEzOjQ0OjAxLjc4NloiLCJ1cGRhdGVkQXQiOiIyMDIyLTAzLTA4VDEzOjQ1OjA2LjMwM1oiLCJfX3YiOjAsInNpZ251cFNvdXJjZSI6IlBSRVBQX0NNUyJ9LCJpc1N0dWRlbnQiOmZhbHNlLCJpYXQiOjE2NTIwOTUyNjN9.JFKFx07xLxQBLGRmTCFDjngJ0ENCQtJ-z3Cdy6cKQ0g'})
    client = Client(transport=transport)
    query = gql('''mutation UploadFiles($files: [Upload!]!) {
    upload(files: $files, type: IMAGE, subType: CONTENT) {
        id
        url
    }
    }''')

    f1 = open(img_path, "rb")
    params = {"files": [f1]}
    result = client.execute(query, variable_values=params, upload_files=True)
    new_url = result['upload']
    img_url = new_url[0]['url']
    img_id = new_url[0]['id']
    return img_id, img_url
    pass

def get_cd_image_details(img_path):
    # base_api = 'https://qa.collegedunia.com/cdprepp-qa/graphql'
    # transport = AIOHTTPTransport(url = base_api, headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7Il9pZCI6IjYyNGMxNzk2ZDVlYzMzNmMzNDIzZTFlOCIsImZpcnN0TmFtZSI6IlByYWJhbCIsImxhc3ROYW1lIjoiR3VwdGEiLCJlbWFpbCI6InByYWJhbC5ndXB0YUBjb2xsZWdlZHVuaWEuY29tIiwibW9iaWxlIjoiKzkxOTE0MDk1NjA5NyIsImVtYWlsVmVyaWZpZWQiOnRydWUsImxhbmd1YWdlIjoiZW4iLCJzdGF0dXMiOiJBQ1RJVkUiLCJyb2xlSWQiOiI2MjNkY2NjMDQyOWM3ZmJmOWNkZWZmOTAiLCJleGFtUHJlZmVyZW5jZXMiOltdLCJuYW1lIjoiUHJhYmFsIEd1cHRhIiwiY3JlYXRlZEF0IjoiMjAyMi0wNC0wNVQxMDoxOTowMi4wODdaIiwidXBkYXRlZEF0IjoiMjAyMi0wNS0wOVQxMToxODo1My44NTdaIiwiX192IjowLCJzaWdudXBTb3VyY2UiOiJQUkVQUF9DTVMiLCJtb2JpbGVWZXJpZmllZCI6dHJ1ZSwiaWQiOiI2MjRjMTc5NmQ1ZWMzMzZjMzQyM2UxZTgifSwiaXNTdHVkZW50IjpmYWxzZSwidG9rZW5UeXBlIjoiQVBJX0FDQ0VTU19UT0tFTiIsImlhdCI6MTY3ODg3MTQ0OH0.nenGku9K-WF3u_lBGX0h9pQDH39UTjQ7iSh_MOzM9X4'})
    # client = Client(transport=transport)
    # query = gql('''mutation UploadFiles($files: [Upload!]!) {
    # upload(files: $files, type: IMAGE, subType: CONTENT) {
    #     id
    #     url
    # }
    # }''')

    # f1 = open(img_path, "rb")
    # params = {"files": [f1]}
    # result = client.execute(query, variable_values=params, upload_files=True)
    # new_url = result['upload']
    # img_url = new_url[0]['url']
    # img_id = new_url[0]['id']
    # return img_id, img_url
    return 1,'https://fakeimagepath'

def cleaning_image_part(img_html,img_count):
    local_image_path = "/home/binoy/second_answers/sample_image.jpg"
    url = img_html.attrs['src']
    if 'http' in url:
        img = requests.get(url)
        with open(local_image_path, 'wb') as f:
            f.write(img.content)
    else:
        url = url.replace('data:image/png;base64,','')
        decoded_data=base64.b64decode((url))
        with open(local_image_path, 'wb') as f:
            f.write(decoded_data)
        
    img_id,img_url = get_cd_image_details(local_image_path)
    final_html = '''<figure class="image"><img src="%s"></figure>'''%(img_url)
    return {img_count:final_html}
