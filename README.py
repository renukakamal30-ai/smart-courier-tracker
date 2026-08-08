# Courier Tracking System

A simple command-line Courier Tracking System built with **Python** and **SQLite**.

The application allows users to create courier shipments, automatically generate tracking IDs, update delivery status, and track packages through every stage of the delivery process.

## Features

- Add new courier shipments
- Automatically generate unique tracking IDs
- Store courier information in SQLite
- Track packages using a tracking ID
- Update delivery status
- Maintain complete tracking history
- Record package location and remarks
- Prevent delivery status from moving backwards
- Enforce delivery stages in the correct order
- Display delivery progress
- View all courier records
- Automatically create the SQLite database
- No external Python packages required

## Delivery Stages

Every courier follows these delivery stages:

```text
1. Booked
       ↓
2. Picked Up
       ↓
3. In Transit
       ↓
4. Arrived at Hub
       ↓
5. Out for Delivery
       ↓
6. Delivered