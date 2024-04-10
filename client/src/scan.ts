export interface Scan {
  id: string
  domain: string
  started_at: string
  completed_at: string
}

export type Result = {
  tool: string
} & (
  | { type: "domain"; value: string }
  | { type: "ip_address"; value: string }
  | { type: "email"; value: string }
  | { type: "url"; value: string }
  | { type: "asn"; value: string }
  | { type: "open_port"; value: string }
  | { type: "technology"; value: { host: string; technology: string } }
  | { type: "social"; value: { platform: string; url: string } }
)

export type ScanWithResults = Scan & {
  results: Result[]
}
