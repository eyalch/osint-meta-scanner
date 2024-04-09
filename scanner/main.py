import uuid

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from . import schemas, service, tasks
from .database import Session

app = FastAPI()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@app.post("/scans", response_model=schemas.Scan)
async def create_scan(data: schemas.ScanCreate, db: Session = Depends(get_db)):
    if service.check_in_progress_scan(db, data.domain):
        raise HTTPException(
            status_code=400,
            detail={
                "error": "A scan for the given domain is already in progress",
                "error_code": "scan_in_progress",
                "domain": data.domain,
            },
        )

    scan = service.create_scan(db, data.domain)

    tasks.scan.delay(scan.id)

    return scan


@app.get("/scans", response_model=list[schemas.Scan])
async def get_scans(db: Session = Depends(get_db)):
    return service.get_scans(db)


@app.get("/scans/{scan_id}", response_model=schemas.ScanWithResults)
async def get_scan(scan_id: uuid.UUID, db: Session = Depends(get_db)):
    scan = service.get_scan(db, scan_id)

    if scan is None:
        raise HTTPException(status_code=404, detail="Scan not found")

    return scan


@app.get("/scans/{scan_id}/results")
async def get_scan_results(scan_id: uuid.UUID, db: Session = Depends(get_db)):
    scan = service.get_scan(db, scan_id)

    if scan is None:
        raise HTTPException(status_code=404, detail="Scan not found")

    return StreamingResponse(
        service.generate_results_csv(scan.results),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{scan_id}.csv"'},
    )
