# CampusLink

CampusLink is a modern campus service management platform built with Django REST Framework (backend) and Vue.js (frontend). The app helps students easily access and manage campus facilities such as Entrepreneur-Hub, Laundry, Central Departmental Store (CDS), and more, all in one place.

## Features

- **Role-based auth**: Login as **User**, **CDS Owner**, **Laundry Admin**, or **Entrepreneur Admin**.
- **User Dashboard**: Modular cards for CDS, Laundry, and Entrepreneur Hub.
- **CDS Storefront**:
  - Browse items with prices
  - Place orders and choose **Cash on Pickup** or **Bkash**
  - View **ETA**, receive an order number, then pick up your food

- **Entrepreneur Hub**:
  - Explore multiple entrepreneur storefronts
  - Each storefront displays product listings and allows orders or contact

- **Laundry Service**:
  - Fill form with cloth category, quantity, and service options (wash, iron, both)
  - Automatically generates an invoice


## Tech Stack

- **Frontend:** Vue 3 (Composition API), Axios, Tailwind CSS
- **Backend:** Django REST Framework
- **Database:**  PostgreSQL

## Getting Started

Project setup and installation instructions are provided in [`setup_guide.md`](./setup_guide.md).



