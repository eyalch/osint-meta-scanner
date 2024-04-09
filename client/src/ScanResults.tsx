import { useMemo, useState } from "react"

import { Result, resultTypeMap } from "./scan.ts"

const toolNameMap: Record<string, string> = {
  amass: "Amass",
  theharvester: "theHarvester",
}

interface ScanResultsProps {
  results: Result[]
  onClose: () => void
}

export default function ScanResults({ results, onClose }: ScanResultsProps) {
  const [tool, setTool] = useState("")

  const tools = useMemo(
    () => Array.from(new Set(results.map((r) => r.tool))),
    [results],
  )

  const resultsByType = useMemo(() => {
    const _resultsByType = Object.fromEntries(
      Object.keys(resultTypeMap).map((type) => [type, new Set<string>()]),
    )

    for (const result of results) {
      if (!tool || result.tool === tool) {
        _resultsByType[result.type].add(result.value)
      }
    }

    return Object.fromEntries(
      Object.entries(_resultsByType).map(([type, results]) => [
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

          {tools.map((tool) => (
            <option key={tool} value={tool}>
              {toolNameMap[tool] || tool}
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
