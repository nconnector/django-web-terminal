from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from dash_kijiji.consumers import MessageConsumer

application = ProtocolTypeRouter({  # which protocol is being used

    "websocket": URLRouter([
                            path("notifications/", MessageConsumer),
    ])
})


# application(environ, start_response):
# environ - dictionary of data
# ...
# start_response() - callable to send headers and response back
# yield data


# application (scope)