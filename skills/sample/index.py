from ask_sdk_core.response_helper import get_text_content
from ask_sdk_model.interfaces.display import (
    RenderTemplateDirective,
    BodyTemplate1)
from azero_sdk.skill_adapter import AzeroSkillAdapter
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

from azero_ipdb.ipdb_util import ipdb_city
from azero_log.azero_logger import logger
try:
    import mock
except ImportError:
    from unittest import mock

DATETIMEFORMAT="%Y-%m-%dT%H:%M:%SZ"

sb = SkillBuilder()
table_name = 'mongo-adapter'

class IntentRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        ip = handler_input.request_envelope.session.attributes['ip']
        city = ipdb_city.find_info(ip, "CN").city_name
        print(city)
        speak_output = '欢迎使用技能'
        logger.info(speak_output, request_envelope=handler_input.request_envelope)
        return (
            handler_input.response_builder.add_directive(
                RenderTemplateDirective(
                    BodyTemplate1(
                        title=speak_output,
                        text_content=get_text_content(primary_text=speak_output))))
                .speak(speak_output)
                .set_should_end_session(True)
                .response
        )

"""
Dialog委托场景COMPLETED完成之后Skill完成当前意图 Handle
若完成当前意图后希望转到新意图set_should_end_session需设为false，且需返回Dialog的Directive
"""
class CompletedDelegateHandler_hello(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (ask_utils.is_request_type("IntentRequest")(handler_input) and
               ask_utils.is_intent_name("hello")(handler_input) and
               ask_utils.get_dialog_state(handler_input).value == 'COMPLETED')
    def handle(self, handler_input):
        currentIntent = handler_input.request_envelope.request.intent
        city = ask_utils.get_slot(handler_input, "city")
        animal = ask_utils.get_slot(handler_input, "animal")
        speakOutput = '欢迎使用技能,您可根据当前意图和槽位返回您想回复的话术';
        logger.info(speakOutput, request_envelope=handler_input.request_envelope)
        logger.warn
        return (
        	handler_input.response_builder
        		.speak(speakOutput)
        		.set_should_end_session(True)
        		.response
        )


"""
用户取消和退出或者错误退出时的Handle
"""
class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.set_should_end_session(True).response

def invoke_skill(app):
    sb.add_request_handler(CompletedDelegateHandler_hello())

    sb.add_request_handler(SessionEndedRequestHandler())
    sb.add_request_handler(IntentRequestHandler())
    skill_adapter = AzeroSkillAdapter(skill=sb.create(), skill_id='5e1c267d48455400095dab42', app = app)
    result = skill_adapter.dispatch_request()
    return result