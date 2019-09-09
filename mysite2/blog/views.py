from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from django.utils import timezone
from blog.forms import PostForm


def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', 
                  {'posts':posts})
    
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', 
                  {'post':post})

def post_new(request):
    # request.method는 현재 이 함수를 실행하기 위해 들어온 요청이
    # POST 방식이라면 문자열 "POST"를 , GET방식이라면 "GET"
    # 를 출력한다. 따라서 POST 방식인지를 구분부터 해준다.
    if request.method == "POST":
        # form 변수에 빈 칸이 채워진 Form 양식을 받아옴
        form = PostForm(request.POST)
        # .is_valid()는 form에서 요청한 자료가 모두 기입되었는지
        # 체크한느 매서드, 만약 모두 기입되지 않았다면 False
        # 모두 기입되었다면 True를 반환한다.
        if form.is_valid() :
            # .save()는 아무것도 입력을 안하면 DB에 바로 
            # 데이터를 적재해버리기 때문에 우선 form 양식 이외에
            # 작성자, 퍼블리싱 시간을 추가 적재하기 위해 임시로
            # DB에 올리기만 하기 위해 commit=False
            post = form.save(commit=False)
            # 현재 로그인된 유저를 글쓴이 정보에 저장
            post.author = request.user
            # 퍼블리싱 날짜는 현재 시간으로 저장
            post.published_date = timezone.now()
            # 모든 작업 완료 후 실제 DB에 저장
            post.save()
            # POST방식으로 들어왔으며, 자료 적재도 완전히 끝나면
            # 쓴 글을 확인할 수 있는 상세페이지로 이동
            # redirect('url 패턴', 우아한 url변수명=넣을자료)
            return redirect('post_detail', pk=post.pk)
        
    # 폼 작성시 어떤 양식을 따라갈 것인지 지정
    # 현재 우리가 forms.py에 작성한 PostForm을 활용해
    # 폼을 자동으로 구성할 예정임
    else:
        # get 방식으로 들어오는 경우는 자료를 반영하지 않고
        # 그냥 다시 post방식 작성을 유도하기 위해 폼으로
        # 이동시키는 로직 실행
        form = PostForm()
    # render에서는 먼저 템플릿 파일 연결 후 폼 정보를 가진
    # form 변수를 같이 넘겨준다.
    return render(request, 'blog/post_edit.html', {'form':form})

# 수정용 폼을 출력해주기 위한 함수
def post_edit(request, pk):
    # 수정 로직은 두 단계를 거칩니다.
    # 1. 수정할 글 정보 받아와서 폼에 전달해 미리 기존 글 내용 기입해두기
    # 2. 사용자가 수정한 다음 제출한 자료로 DB에 갱신하기
    # 1번 로직이라면 기존 글 정보를 받아오기 위해 get_object_or_404를
    # 2번 로직이라면 폼에서 받아온 정보를 기존자료에 덮어씌우기 위해서
    # get_object_or_404를 실행해야 합니다.
    post = get_object_or_404(Post, pk=pk)
    # POST 방식 요청을 form의 제출버튼을 통해서만 이루어질 수 있음
    # 따라서 수정완료 후 제출버튼을 눌렀을 때만 POST방식으로 인식됨
    if request.method == "POST":
        # 수정완료된 경우는 새롭게 들어온 자료를 기존자료에 덮어씌움
        # 폼이름(request.POST(갱신자료), instance=기존자료)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            # 폼에서 제출된 자료가 글제목, 본문 뿐이므로
            # 다시 글쓴이 정보와 글 배포시간을 갱신. 단 이경우는
            # 새롭게 글을 쓰는 것이 아니라 글 생성시간은 변경 X
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            # 수정완료시는 post_edit(수정양식 템플릿)이 아닌
            # post_detail(수정 결과를 볼 수 있는 템플릿)으로 이동
            return redirect('post_detail', pk=post.pk)
    else:
        # GET방식 요청인 경우는 기존 글에 적혀있던 정보만
        # form에 대입해주고 추가적인 로직을 실행할 필요는 없음
        form = PostForm(instance=post)
        # 수정을 시작하는 경우 post_edit(수정양식 템플릿)
        # 에 기존글에 대한 정보(form)을 함께 넘겨줌
    return render(request, 'blog/post_edit.html', {'form':form})

# 몇 번 글을 삭제하는지 요청받기 위해서 pk를 입력받음
def post_remove(request, pk):
    # 삭제할 글 정보 가져오기
    post = get_object_or_404(Post, pk=pk)
    # 삭제시는 가져온 글 정보.delete()만으로 간단하게 삭제가 가능하다
    post.delete()
    # 삭제한 다음은 글 목록 페이지로 돌아가준다.
    return redirect('post_list')
    
        