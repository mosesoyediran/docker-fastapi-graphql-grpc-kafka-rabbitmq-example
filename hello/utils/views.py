from fastapi import APIRouter, Request, status

router = APIRouter(prefix="/utils", tags=["utils"])


@router.api_route("/ping-kafka",methods=["GET", "POST"], status_code=status.HTTP_202_ACCEPTED)
async def ping_kafka(request: Request):
    producer = getattr(request.app.state, "producer", None)
    if producer is None:
        return {"error": "Kafka disabled"}

    await producer.send_and_wait("hello_topic", b"pong")
    return {"status": "sent"}
