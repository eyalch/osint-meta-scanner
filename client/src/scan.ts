export interface Scan {
  id: string
  domain: string
  started_at: string
  completed_at: string
}

export const resultTypeMap: Record<string, string> = {
  domain: "Domains",
  ip_address: "IP addresses",
  email: "Emails",
  url: "URLs",
  asn: "ASNs",
}

export interface Result {
  tool: string
  type: string
  value: string
}

export type ScanWithResults = Scan & {
  results: Result[]
}
