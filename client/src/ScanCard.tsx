import { useQuery } from "@tanstack/react-query"
import axios from "axios"
import { formatDuration, intervalToDuration } from "date-fns"
import { useRef } from "react"

import Dialog, { DialogRef } from "./Dialog.tsx"
import ScanResults from "./ScanResults.tsx"
import { Scan, ScanWithResults } from "./scan.ts"

interface ScanCardProps {
  scan: Scan
}

export default function ScanCard({ scan }: ScanCardProps) {
  const dialogRef = useRef<DialogRef>(null)

  const resultsQuery = useQuery({
    queryKey: ["scans", scan.id],
    queryFn: () =>
      axios
        .get<ScanWithResults>(`/api/scans/${scan.id}`)
        .then((res) => res.data),
    select: (data) => data.results,
    enabled: false,
  })

  return (
    <article>
      <section>
        <div>ID</div>
        <span style={{ fontFamily: "monospace" }}>{scan.id}</span>
      </section>

      <section>
        <div>Domain</div>
        <strong>{scan.domain}</strong>
      </section>

      <section>
        <div>Started at</div>
        <strong>
          {scan.started_at ? new Date(scan.started_at).toLocaleString() : "–"}
        </strong>
      </section>

      <section>
        <div>Completed at</div>
        {scan.completed_at ? (
          <>
            <strong>{new Date(scan.completed_at).toLocaleString()}</strong>
            &nbsp;(
            {formatDuration(
              intervalToDuration({
                start: scan.started_at,
                end: scan.completed_at,
              }),
              { delimiter: ", " },
            )}
            )
          </>
        ) : (
          <strong>–</strong>
        )}
      </section>

      <footer style={{ display: "flex", gap: "var(--pico-spacing)" }}>
        <button
          aria-busy={resultsQuery.isFetching}
          onClick={() =>
            void resultsQuery
              .refetch({ throwOnError: true })
              .then(dialogRef.current?.showModal)
          }
        >
          View
        </button>

        <a
          href={`/api/scans/${scan.id}/results/export`}
          role="button"
          className="outline"
        >
          Export results
        </a>
      </footer>

      <Dialog ref={dialogRef}>
        {resultsQuery.data ? (
          <ScanResults
            results={resultsQuery.data}
            onClose={() => dialogRef.current?.close()}
          />
        ) : null}
      </Dialog>
    </article>
  )
}
