
# CCODEL_Tickets
# Hiiiiii
=======
# Project Setup Guide

## Prerequisites
To set up this project, you need **pnpm** installed.

### Install pnpm
If you don't have **pnpm** installed, run the following command:
```bash
npm install -g pnpm
```
For more installation methods, visit the [pnpm website](https://pnpm.io/installation).

## Cloning the Repository
1. Clone the repository:
```bash
git clone [<repository-url>](https://github.com/Bluel0la/ccodel_tickets.git)
cd ccodel_tickets
cd frontend
```

2. Install dependencies:
```bash
pnpm install
```

3. Start the development server:
```bash
pnpm  run dev
```

## Folder Structure
Each developer is assigned specific folders:
- **Components Folder:** Contains reusable components.
- **Pages Folder:** Contains individual pages for different roles.

### Routing in `App.jsx`
The `App.jsx` file is strictly for defining routes. Each route must be placed in the designated section:
```jsx
{/* Student Routes */}
{/*<Route path="/student/pagename" element={}/>*/}
{/* Student Routes */}

{/* Support Staff Routes */}
{/*<Route path="/support/pagename" element={}/>*/}
{/* Support Staff Routes */}

{/* Admin Routes */}
{/*<Route path="/admin/pagename" element={}/>*/}
{/* Admin Routes */}
```

## Collaboration Process
1. **Pull Changes** from the main branch before starting new work:
```bash
git pull origin master
```

2. Create a **New Branch** for your feature or fix:
```bash
git checkout -b feature/your-feature-name
```

3. Commit your changes:
```bash
git add .
git commit -m "Your commit message"
```

4. Push your branch:
```bash
git push origin feature/your-feature-name
```

5. Create a **Pull Request** to the `main` branch.

6. Wait for the **Admin Reviewer** to review and merge your changes.

---
This guide ensures a smooth and consistent workflow across all contributors.

