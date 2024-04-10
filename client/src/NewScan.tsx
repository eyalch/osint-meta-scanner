import { useMutation } from "@tanstack/react-query"
import axios from "axios"
import { useRef, useState } from "react"

import Dialog, { DialogRef } from "./Dialog.tsx"

function isScanInProgressError(error: unknown) {
  return Boolean(
    axios.isAxiosError<unknown>(error) &&
      error.response?.data &&
      typeof error.response.data === "object" &&
      "detail" in error.response.data &&
      error.response.data.detail &&
      typeof error.response.data.detail === "object" &&
      "error_code" in error.response.data.detail &&
      error.response.data.detail.error_code === "scan_in_progress",
  )
}

interface NewScanProps {
  onSubmitted: () => void
}

export default function NewScan({ onSubmitted }: NewScanProps) {
  const [domain, setDomain] = useState("")

  const mutation = useMutation({
    mutationFn: async (domain: string) => {
      await axios.post("/api/scans", { domain })

      // Wait for a bit to allow the server to start the scan and assign a `started_at` timestamp.
      await new Promise((resolve) => setTimeout(resolve, 500))
    },
  })

  const dialogRef = useRef<DialogRef>(null)

  const isScanInProgress =
    mutation.isError && isScanInProgressError(mutation.error)

  return (
    <section>
      <h1>New scan</h1>

      <button onClick={() => dialogRef.current?.showModal()}>Scan</button>

      <Dialog ref={dialogRef}>
        <article>
          <header>
            <button
              aria-label="Close"
              rel="prev"
              onClick={() => dialogRef.current?.close()}
            ></button>

            <strong>Scan</strong>
          </header>

          <form
            id="scan-form"
            onSubmit={(event) => {
              event.preventDefault()

              void mutation.mutateAsync(domain).then(() => {
                dialogRef.current?.close()
                onSubmitted()
              })
            }}
          >
            <label>
              Domain
              <input
                value={domain}
                onChange={(event) => {
                  setDomain(event.target.value)
                }}
                required
                aria-invalid={isScanInProgress || undefined}
                aria-describedby={
                  isScanInProgress ? "scan-in-progress-helper" : undefined
                }
              />
              {isScanInProgress ? (
                <small id="scan-in-progress-helper">
                  A scan for this domain is already in progress
                </small>
              ) : null}
            </label>
          </form>

          <footer>
            <button form="scan-form" aria-busy={mutation.isPending}>
              Scan
            </button>
          </footer>
        </article>
      </Dialog>
    </section>
  )
}
