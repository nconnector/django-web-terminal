from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from dash_kijiji.consumers import MessageConsumer

application = ProtocolTypeRouter({  # which protocol is being used

    "websocket": URLRouter([
                            path("notifications/", MessageConsumer),
    ])
})