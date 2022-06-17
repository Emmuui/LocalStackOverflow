from question.serializers import OutputQuestionSerializer


def get_output_serializer(data):
    print(f'data =========== {data}')
    output_serializer = OutputQuestionSerializer(data=data)
    output_serializer.is_valid(raise_exception=True)
    return output_serializer
