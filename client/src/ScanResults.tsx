import { useMemo, useState } from "react"

import { Result } from "./scan.ts"

const tools: Record<string, string> = {
  amass: "Amass",
  theharvester: "theHarvester",
  bbot: "BBOT",
}

const resultTypeMap: Record<string, string> = {
  domain: "Domains",
  ip_address: "IP addresses",
  email: "Emails",
  url: "URLs",
  asn: "ASNs",
  open_port: "Open Ports",
  technology: "Technologies",
  social: "Social Accounts",
}

interface ScanResultsProps {
  results: Result[]
  onClose: () => void
}

export default function ScanResults({ results, onClose }: ScanResultsProps) {
  const [tool, setTool] = useState("")

  const resultsByType = useMemo(() => {
    const byType = Object.fromEntries(
      Object.keys(resultTypeMap).map((type) => [type, new Set<string>()]),
    )

    const filteredResults = tool
      ? results.filter((r) => r.tool === tool)
      : results

    for (const result of filteredResults) {
      switch (result.type) {
        case "technology":
          byType[result.type].add(
            `${result.value.technology} (${result.value.host})`,
          )
          break

        case "social":
          byType[result.type].add(result.value.url)
          break

        default:
          byType[result.type].add(result.value)
      }
    }

    return Object.fromEntries(
      Object.entries(byType).map(([type, results]) => [
        type,
        Array.from(results),
      ]),
    )
  }, [results, tool])

  return (
    <article>
      <header>
        <button
          aria-label="Close"
          rel="prev"
          onClick={() => {
            onClose()
          }}
        ></button>

        <strong>Results</strong>
      </header>

      <h2>Results</h2>

      <label>
        Scanner
        <select
          value={tool}
          onChange={(event) => {
            setTool(event.target.value)
          }}
        >
          <option value="">All</option>

          {Object.entries(tools).map(([id, name]) => (
            <option key={id} value={id}>
              {name}
            </option>
          ))}
        </select>
      </label>

      {Object.entries(resultsByType).map(([type, resultsForType]) => (
        <section key={type}>
          <h3>
            {resultTypeMap[type]} ({resultsForType.length})
          </h3>

          {resultsForType.length > 0 ? (
            <ul>
              {resultsForType.map((value) => (
                <li key={value}>{value}</li>
              ))}
            </ul>
          ) : (
            <p>No results</p>
          )}
        </section>
      ))}
    </article>
  )
}
