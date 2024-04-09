import { useQuery } from "@tanstack/react-query"
import axios from "axios"

import NewScan from "./NewScan.tsx"
import ScanCard from "./ScanCard.tsx"
import { Scan } from "./scan.ts"

export default function App() {
  const scansQuery = useQuery({
    queryKey: ["scans"],
    queryFn: () => axios.get<Scan[]>("/api/scans").then((res) => res.data),
  })

  return (
    <>
      <header>
        <nav>
          <ul>
            <li>
              <strong>OSINT Meta Scanner</strong>
            </li>
          </ul>
        </nav>
      </header>

      <main>
        <NewScan onSubmitted={() => void scansQuery.refetch()} />

        <section>
          <h1>Most recent scans</h1>

          {scansQuery.isLoading ? (
            <span aria-busy="true">Loading scans…</span>
          ) : scansQuery.isError ? (
            <p>Error loading scans</p>
          ) : scansQuery.data ? (
            scansQuery.data.map((scan) => (
              <ScanCard key={scan.id} scan={scan} />
            ))
          ) : null}
        </section>
      </main>
    </>
  )
}
