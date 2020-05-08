# Create your API endpoints here
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND

from rewards.models import RecommendedReward, User
from rewards.serializers import RecommendedRewardSerializer


@api_view(['GET'])
def recommendations(request, user_id):
    try:
        User.objects.get(pk=user_id)
        query_result = RecommendedReward.objects.filter(user_id=user_id)
        return Response(data=dict(rewards=RecommendedRewardSerializer(query_result, many=True).data))
    except User.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND,data="User does not exist")

