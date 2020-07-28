from azero_sdk_core.response_helper import get_text_content
from azero_sdk_model.interfaces.display import (
    RenderTemplateDirective,
    BodyTemplate1)
from azero_sdk_model.dialog import *
from azero_sdk_core.skill_builder import SkillBuilder
from azero_sdk_core.dispatch_components import AbstractRequestHandler
import azero_sdk_core.utils as ask_utils
from azero_sdk_core.handler_input import HandlerInput
from azero_sdk_model import Response
from azero_sdk.skill_adapter import AzeroSkillAdapter

sb = SkillBuilder()


"""
Azero系统根据您自定义意图的意图标识自动生成此函数。
can_handle:判断传入此意图的请求是否要被此函数处理。默认判断规则为：请求中的意图标识与本意图标识匹配，且用户与技能一次对话交互已经完成(即DialogState为COMPLETED)。
handle:当can_handle返回为true时,自动执行。开发者需在handle内部编写此意图的业务逻辑代码。
用户与技能对话交互过程(DialogState)，有三种状态:STARTED、IN_PROGRESS、COMPLETED。若意图不涉及多轮对话即可只关注COMPLETED状态。
若完成当前意图后希望转到新意图withShouldEndSession需设为false，且需返回Dialog的Directive。
"""
class CompletedDelegateHandler_hello(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (ask_utils.is_request_type("IntentRequest")(handler_input) and
               ask_utils.is_intent_name("test")(handler_input) and
               ask_utils.get_dialog_state(handler_input).value == 'COMPLETED')
    def handle(self, handler_input):
        currentIntent = handler_input.request_envelope.request.intent
        speakOutput = '欢迎使用技能,您可根据当前意图和槽位返回您想回复的话术'
        return (
        	handler_input.response_builder
        		.speak(speakOutput)
        		.set_should_end_session(True)
        		.response
        )

"""
Azero系统根据您自定义意图的意图标识以及您意图选用了禁用自动委派，自动生成此函数。
若您的交互不涉及多轮对话(一问一答即完成对话)或对话交互业务复杂度可以完全委托给Azero系统根据前端意图配置中的澄清话术、意图确认等处理整个对话，建议您开启自动委派
功能，忽略此函数。
can_handle:判断传入此意图的请求是否要被此函数处理。默认判断规则为:请求中的意图标识与本意图标识匹配，且用户与技能对话交互还处于中间状态(DialogState为STARTED或IN_PROGRESS)。
handle:当can_handle返回为true时,自动执行。由于意图禁用了自动委派，那么用户与技能对话交互过程，若有澄清话术，意图确认等需求，Azero会把此类请求传入此函数，您
可以在此通过代码，手动对澄清话术，验证槽位，确定槽位和确定意图等业务做特殊处理。
用户与技能对话交互过程(DialogState)，有三种状态:STARTED、IN_PROGRESS、COMPLETED。
若完成当前意图后希望转到新意图withShouldEndSession需设为false，且需返回Dialog的Directive。
"""
class CombineDialogDelegateHandler_hello(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (ask_utils.is_request_type("IntentRequest")(handler_input) and
               ask_utils.is_intent_name("test")(handler_input) and
               (ask_utils.get_dialog_state(handler_input).value == 'STARTED' or
               ask_utils.get_dialog_state(handler_input).value == 'IN_PROGRESS'))
    def handle(self, handler_input):
        currentIntent = handler_input.request_envelope.request.intent
        speakOutput = '您可根据判断意图或者所有槽位返回您想回复的话术和模版'
#        handler_input.response_builder.add_directive(ElicitSlotDirective(currentIntent, "槽位名称"))
#        handler_input.response_builder.add_directive(ConfirmSlotDirective(currentIntent, "槽位名称"))
#        handler_input.response_builder.add_directive(DelegateDirective(currentIntent))
#        handler_input.response_builder.add_directive(ConfirmIntentDirective(currentIntent))
        return (
        	handler_input.response_builder
        		.add_directive(DelegateDirective(currentIntent))
        		.speak(speakOutput)
        		.set_should_end_session(False)
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

        return handler_input.response_builder.speak('已退出当前意图').set_should_end_session(True).response

class IntentRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        speak_output='欢迎使用技能'
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
所有意图函数都需要添加到add_request_handler中。保证Azero系统能正常将用户的意图请求传入
对应的意图函数中进行处理。服务部署一般会自动生成添加代码。
"""
def invoke_skill(app):
    sb.add_request_handler(CompletedDelegateHandler_hello())
    sb.add_request_handler(CombineDialogDelegateHandler_hello())

    sb.add_request_handler(SessionEndedRequestHandler())
    sb.add_request_handler(IntentRequestHandler())
    skill_adapter = AzeroSkillAdapter(skill=sb.create(), skill_id='sample', app = app)
    result = skill_adapter.dispatch_request()
    return result