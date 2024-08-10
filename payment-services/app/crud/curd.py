from fastapi import HTTPException
import stripe


async def create_payment_intent(amount: int, user):
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            payment_method_types=["card"],
        )
        return {"client_secret": payment_intent["client_secret"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
