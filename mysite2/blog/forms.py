from django import forms

from .models import Post

# 폼을 지정해서 만들때는 class를 이용해서 만들게 됩니다.
# forms.Modelform을 괄호 내부에 넣어주셔야합니다.
class PostForm(forms.ModelForm):
    # Post모델에 자료를 집어넣어주기 위한 세부사항은
    # PostForm 클래스 내부에 다시 Meta라는 클래스를 선언해서
    # 작성하게 됩니다.
    class Meta :
        # model 변수에는 어떤 모델(창고)이 타겟인지
        model = Post
        # fields 변수에는 튜플형태로 어떤 요소를 사용자가
        # 직접 입력하게 할지를 문자열로 적어줍니다.
        fields = ('title', 'text')
     