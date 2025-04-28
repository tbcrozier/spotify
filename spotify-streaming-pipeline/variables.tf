# variables.tf

variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "Region for resources"
  type        = string
  default     = "us-central1"
}

variable "dataset_id" {
  description = "BigQuery dataset ID"
  type        = string
  default     = "spotify_streaming"
}

variable "table_id" {
  description = "BigQuery table ID"
  type        = string
  default     = "now_playing"
}

variable "pubsub_topic" {
  description = "Pub/Sub topic for Spotify events"
  type        = string
  default     = "spotify-now-playing"
}
