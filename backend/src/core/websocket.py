from typing import Dict
from fastapi import WebSocket
from redis import Redis


class ConnectionManager:
    def __init__(self, redis_client: Redis):
        # Store active WebSocket connections: {group_id: {user_id: WebSocket}}
        self.active_connections: Dict[str, Dict[str, WebSocket]] = {}
        self.redis = redis_client

    async def connect(self, websocket: WebSocket, group_id: str, user_id: str):
        """Connect a user to a group's WebSocket."""
        await websocket.accept()

        # Initialize group dict if not exists
        if group_id not in self.active_connections:
            self.active_connections[group_id] = {}

        # Store the WebSocket connection
        self.active_connections[group_id][user_id] = websocket

        # Broadcast join message to group
        await self.broadcast_to_group(group_id, {"type": "PLAYER_JOINED", "data": {"user_id": user_id}})

    async def disconnect(self, group_id: str, user_id: str):
        """Disconnect a user from a group's WebSocket."""
        # Remove the connection
        if group_id in self.active_connections:
            self.active_connections[group_id].pop(user_id, None)

            # Remove group if empty
            if not self.active_connections[group_id]:
                self.active_connections.pop(group_id)
            else:
                # Broadcast leave message to remaining users
                await self.broadcast_to_group(group_id, {"type": "PLAYER_LEFT", "data": {"user_id": user_id}})

    async def broadcast_to_group(self, group_id: str, message: dict):
        """Broadcast a message to all users in a group."""
        if group_id in self.active_connections:
            # Publish to Redis for other server instances
            await self.redis.publish(f"group:{group_id}", str(message))

            # Send to all WebSocket connections in this group
            for connection in self.active_connections[group_id].values():
                await connection.send_json(message)

    async def send_personal_message(self, group_id: str, user_id: str, message: dict):
        """Send a message to a specific user in a group."""
        if group_id in self.active_connections and user_id in self.active_connections[group_id]:
            await self.active_connections[group_id][user_id].send_json(message)

    def get_active_users(self, group_id: str) -> list:
        """Get list of active user IDs in a group."""
        if group_id in self.active_connections:
            return list(self.active_connections[group_id].keys())
        return []

    async def broadcast_game_start(self, group_id: str, question_data: dict):
        """Broadcast game start with question to all users in a group."""
        await self.broadcast_to_group(group_id, {"type": "ROUND_STARTED", "data": question_data})

    async def broadcast_round_results(self, group_id: str, results: dict):
        """Broadcast round results to all users in a group."""
        await self.broadcast_to_group(group_id, {"type": "ROUND_RESULTS", "data": results})
