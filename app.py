from flask import Flask, render_template, jsonify, request
import requests
""" Flask : Flask 웹 프레임워크를 사용하기 위한 모듈
render_template : HTML 템플릿을 렌더링하기 위한 함수
jsonify : 데이터를 JSON 형식으로 반환하기 위한 함수
request :  HTTP 요청 데이터를 처리하기 위한 객체
requests : HTTP 요청을 보내기 위한 라이브러리 """

# Flask 애플리케이션을 생성
app = Flask(__name__)


# Velog의 GraphQL API를 사용하여 특정 사용자의 글 목록을 가져옴
# cursor를 사용하여 페이징을 처리
def fetch_posts(username, cursor=None):
    url = 'https://v3.velog.io/graphql'

    # headers : 요청 헤더를 설정
    headers = {
        'content-type': 'application/json',
        'accept': '*/*',
        'origin': 'https://velog.io',
        'referer': 'https://velog.io/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
    }

    # query : GraphQL 쿼리를 정의
    query = """
    query velogPosts($input: GetPostsInput!) {
      posts(input: $input) {
        id
        title
        url_slug
        user {
          username
        }
      }
    }
    """

    # variables : GraphQL 쿼리에 사용할 변수를 설정
    variables = {
        'input': {
            'username': username,
            'limit': 10,
            'tag': ''
        }
    }
    if cursor:
        variables['input']['cursor'] = cursor

    # payload : 요청 본문을 JSON 형식으로 설정
    payload = {
        'query': query,
        'variables': variables
    }

    # response : HTTP POST 요청을 보내고 응답을 받음
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    # data : 응답 데이터를 JSON 형식으로 파싱
    data = response.json()
    return data['data']['posts']

# 특정 글의 조회수를 가져오는 함수
# post_id와 access_token을 사용하여 요청을 보냅
def fetch_views(post_id, access_token):
    url = 'https://v2cdn.velog.io/graphql'

    # headers : 요청 헤더를 설정
    # authorization 헤더에 Bearer 토큰을 포함
    headers = {
        'content-type': 'application/json',
        'accept': '*/*',
        'origin': 'https://velog.io',
        'referer': 'https://velog.io/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'authorization': f'Bearer {access_token}'
    }
    query = """
    query GetStats($post_id: ID!) {
      getStats(post_id: $post_id) {
        total
      }
    }
    """
    payload = {
        'query': query,
        'variables': {
            'post_id': post_id
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data['data']['getStats']['total']

# 기본 경로 /에 대해 index.html 템플릿을 렌더링
@app.route('/')
def index():
    return render_template('index.html')

# /api/views/<username> 경로로 GET 요청이 오면 특정 사용자의 글 목록과 조회수를 반환
@app.route('/api/views/<username>', methods=['GET'])
def get_views(username):

    # access_token을 쿼리 매개변수로 받아옴
    access_token = request.args.get('access_token')

    # access_token이 없으면 오류 메시지를 반환
    if not access_token:
        return jsonify({'error': 'Access token is required'}), 400

    # 글 목록을 가져오고, 각 글의 조회수를 가져와 all_views_data 리스트에 추가
    # 모든 글을 가져올 때까지 반복
    all_views_data = []
    cursor = None
    try:
        while True:
            posts = fetch_posts(username, cursor)
            for post in posts:
                post_url = f"https://velog.io/@{username}/{post['url_slug']}"
                views = fetch_views(post['id'], access_token)
                all_views_data.append({
                    'title': post['title'],
                    'url': post_url,
                    'views': views
                })
            if len(posts) < 10:
                break
            cursor = posts[-1]['id']
        return jsonify(all_views_data)
    except Exception as e:
        print(f'Error: {e}')
        # 오류 발생 시 오류 메시지를 JSON 형식으로 반환
        return jsonify({'error': str(e)}), 500

# 애플리케이션을 디버그 모드에서 실행
if __name__ == '__main__':
    app.run(debug=True)