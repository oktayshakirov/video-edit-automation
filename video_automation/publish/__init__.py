"""Publishing a finished render to the platforms, as opposed to making it.

YouTube lives in the `youtube-audit` CLI, because that is where the three
channel tokens already are. Instagram and Facebook live in n8n, because that is
where the Meta credentials already are. TikTok lives here, and this file records
why it is the odd one out: n8n's generic OAuth2 credential sends `client_id`,
while TikTok's token endpoint demands `client_key`, so n8n cannot refresh a
TikTok token without a custom node. Tokens are refreshed here instead.
"""
