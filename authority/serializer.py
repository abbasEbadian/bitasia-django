from rest_framework import serializers

from authority.models import AuthorityRuleOption, AuthorityLevel, AuthorityRule, AuthorityRequest


class AuthorityRuleOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorityRuleOption
        exclude = ('create_date', 'write_date', "max_value", "min_value")


class AuthorityRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorityRule
        exclude = ('create_date', 'write_date', 'option_ids')


class AuthorityRuleWithOptionSerializer(serializers.ModelSerializer):
    options = AuthorityRuleOptionSerializer(source='option_ids', many=True, read_only=True)

    class Meta:
        model = AuthorityRule
        exclude = ('create_date', 'write_date', 'option_ids')


class AuthorityLevelSerializer(serializers.ModelSerializer):
    rules = AuthorityRuleSerializer(source='rule_ids', many=True, read_only=True)

    class Meta:
        model = AuthorityLevel
        exclude = ('create_date', 'rule_ids', 'write_date')


class AuthorityRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorityRequest
        fields = "__all__"
        depth = 1
