print("******** PRACTICE.PY LOADED ********")

from fastapi import APIRouter, HTTPException, UploadFile, File
import cv2
import numpy as np

from app.services.gesture_service import GestureService


router = APIRouter(
    prefix="/practice",
    tags=["Practice"]
)


print("Creating GestureService...")
gesture = GestureService()
print("GestureService Created Successfully.")


# ============================================================
# START PRACTICE
# ============================================================

@router.post("/start")
def start():

    print("\n========== START PRACTICE ==========")

    try:

        result = gesture.start_practice()

        print("Practice Started Successfully.")

        return {
            "success": True,
            "message": "Practice Started",
            "current_letter": gesture.get_current_letter()
        }

    except Exception as e:

        print("\n========== START PRACTICE ERROR ==========")
        print(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# CURRENT LETTER
# ============================================================

@router.get("/current")
def current():

    print("\n========== CURRENT LETTER ==========")

    try:

        letter = gesture.get_current_letter()

        print("Current Letter :", letter)

        return {
            "success": True,
            "current_letter": letter
        }

    except Exception as e:

        print("\n========== CURRENT LETTER ERROR ==========")
        print(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# PREDICT GESTURE FROM BROWSER IMAGE
# ============================================================

@router.post("/predict")
async def predict(
    file: UploadFile = File(...)
):

    print("\n==========================================")
    print("PRACTICE /PREDICT API CALLED")
    print("==========================================")

    try:

        # ----------------------------------------------------
        # STEP 1 — Check uploaded file
        # ----------------------------------------------------

        print("Step 1 : Receiving image")

        if file is None:

            raise HTTPException(
                status_code=400,
                detail="No image file received."
            )

        print("Filename :", file.filename)
        print("Content Type :", file.content_type)

        # ----------------------------------------------------
        # STEP 2 — Read image bytes
        # ----------------------------------------------------

        print("Step 2 : Reading image bytes")

        contents = await file.read()

        if not contents:

            raise HTTPException(
                status_code=400,
                detail="Uploaded image is empty."
            )

        print(
            "Image bytes received :",
            len(contents)
        )

        # ----------------------------------------------------
        # STEP 3 — Convert bytes to NumPy array
        # ----------------------------------------------------

        print("Step 3 : Converting image to NumPy array")

        image_array = np.frombuffer(
            contents,
            dtype=np.uint8
        )

        # ----------------------------------------------------
        # STEP 4 — Decode image using OpenCV
        # ----------------------------------------------------

        print("Step 4 : Decoding image with OpenCV")

        frame = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR
        )

        if frame is None:

            raise HTTPException(
                status_code=400,
                detail="Unable to decode uploaded image."
            )

        print(
            "Frame decoded successfully."
        )

        print(
            "Frame shape :",
            frame.shape
        )

        # ----------------------------------------------------
        # STEP 5 — Send frame to AI Engine
        # ----------------------------------------------------

        print("Step 5 : Running AI prediction")

        prediction_result = gesture.predict_frame(
            frame
        )

        print(
            "Predicted Letter :",
            prediction_result.predicted_label
        )

        print(
            "Confidence :",
            prediction_result.confidence
        )

        print(
            "Inference Time :",
            prediction_result.inference_time_ms
        )

        print(
            "Success :",
            prediction_result.success
        )

        print(
            "Message :",
            prediction_result.message
        )

        # ----------------------------------------------------
        # STEP 6 — Send AI result to AssessmentService
        # ----------------------------------------------------

        print(
            "Step 6 : Processing assessment"
        )

        assessment_result = (
            gesture.process_prediction_result(
                prediction_result
            )
        )

        print(
            "\n========== ASSESSMENT COMPLETED =========="
        )

        print(
            assessment_result
        )

        # ----------------------------------------------------
        # STEP 7 — Return result to frontend
        # ----------------------------------------------------

        print(
            "Step 7 : Returning response to frontend"
        )

        return {
            "success": True,
            **assessment_result
        }

    except HTTPException:

        raise

    except Exception as e:

        print(
            "\n========== PREDICTION ERROR =========="
        )

        print(
            type(e).__name__,
            ":",
            str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# NEXT LETTER
# ============================================================

@router.post("/next")
def next_letter():

    print("\n========== NEXT LETTER ==========")

    try:

        letter = gesture.next_letter()

        print(
            "Next Letter :",
            letter
        )

        return {
            "success": True,
            "next_letter": letter
        }

    except Exception as e:

        print(
            "\n========== NEXT LETTER ERROR =========="
        )

        print(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# SESSION STATISTICS
# ============================================================

@router.get("/statistics")
def statistics():

    print(
        "\n========== SESSION STATISTICS =========="
    )

    try:

        stats = gesture.get_statistics()

        print(stats)

        return stats

    except Exception as e:

        print(
            "\n========== STATISTICS ERROR =========="
        )

        print(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# ATTEMPT HISTORY
# ============================================================

@router.get("/history")
def history():

    print(
        "\n========== ATTEMPT HISTORY =========="
    )

    try:

        attempts = gesture.get_history()

        print(attempts)

        return {
            "success": True,
            "attempts": attempts
        }

    except Exception as e:

        print(
            "\n========== HISTORY ERROR =========="
        )

        print(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# ASSESSMENT REPORT
# ============================================================

@router.get("/report")
def report():

    print(
        "\n========== ASSESSMENT REPORT =========="
    )

    try:

        result = gesture.generate_report()

        print(result)

        return result

    except Exception as e:

        print(
            "\n========== REPORT ERROR =========="
        )

        print(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# PRACTICE REVIEW
# ============================================================

@router.get("/review")
def review():

    print(
        "\n========== PRACTICE REVIEW =========="
    )

    try:

        result = gesture.generate_review()

        print(result)

        return result

    except Exception as e:

        print(
            "\n========== REVIEW ERROR =========="
        )

        print(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# END SESSION
# ============================================================

@router.post("/end")
def end():

    print(
        "\n========== END PRACTICE =========="
    )

    try:

        result = gesture.end_session()

        print(result)

        return result

    except Exception as e:

        print(
            "\n========== END SESSION ERROR =========="
        )

        print(str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )