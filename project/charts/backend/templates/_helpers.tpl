{{/*
Common name. Falls back to the chart name (release-aware helpers omitted for clarity).
*/}}
{{- define "backend.name" -}}
{{- .Chart.Name -}}
{{- end -}}

{{/*
Standard labels applied to every object. Kubernetes recommended label set.
*/}}
{{- define "backend.labels" -}}
app.kubernetes.io/name: {{ include "backend.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
{{- end -}}

{{/*
Selector labels - the SUBSET used for matchLabels / service selectors.
Must stay stable (never templatize with values that change), or you break rollouts.
*/}}
{{- define "backend.selectorLabels" -}}
app.kubernetes.io/name: {{ include "backend.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}
