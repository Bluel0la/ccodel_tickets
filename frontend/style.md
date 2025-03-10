# Style Guide README

## Typography
- **Primary Font Family (Body Text):** DM Sans
- **Title/Heading Font Family:** Merriweather

## Color Palette
### Primary Colors
- **Blue:** `#3b4794`
- **Turkish Blue 1:** `#3179bc`
- **Turkish Blue 2:** `#6695c8`
- **Light Steel Blue:** `#bacbef3`
- **White:** `#ffffff`

### Secondary Colors
- **Soft Beige:** `#e6c5b1`

## Usage Guidelines
- **Headings** should use **Merriweather** with a slightly larger size and bold weight.
- **Body Text** should be set in **DM Sans** for clarity and readability.
- **Primary Buttons** should use **Blue (#3b4794)** as the background with **White (#ffffff)** text.
- **Hover States** for buttons can use **Turkish Blue 1 (#3179bc)**.
- **Background Sections** can alternate between **Light Steel Blue (#bacbef3)** and **White (#ffffff)** for a subtle contrast.
- Use **Soft Beige (#e6c5b1)** sparingly for highlights or accents.

## Example Styling
```css
body {
  font-family: 'DM Sans', sans-serif;
  color: #3b4794;
  background-color: #ffffff;
}
h1, h2, h3 {
  font-family: 'Merriweather', serif;
  color: #3b4794;
}
button {
  background-color: #3b4794;
  color: #ffffff;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
}
button:hover {
  background-color: #3179bc;
}
```

## Accessibility Considerations
- Maintain a contrast ratio of at least **4.5:1** between text and background colors.
- Use **alt text** for all images.
- Ensure all interactive elements are keyboard accessible.

---
This guide helps maintain consistency and visual harmony throughout the project.

