import React from "react";

const KnowledgeBase = () => {
  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-400 to-purple-500 text-white p-6">
      <header className="text-center mb-8">
        <h1 className="text-4xl font-bold">How can we help?</h1>
        <input 
          type="text" 
          placeholder="Try 'reset password' or 'custom themes'" 
          className="mt-4 bg-white w-full max-w-md p-3 rounded-md text-gray-800 shadow-lg focus:outline-none"
        />
      </header>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {sections.map((section, index) => (
          <div 
            key={index} 
            className="p-6 rounded-lg shadow-lg flex flex-col items-center text-center bg-white text-gray-900"
          >
            <div 
              className="w-16 h-16 flex items-center justify-center text-3xl rounded-full mb-4"
              style={{ backgroundColor: section.color }}
            >
              {section.icon}
            </div>
            <h3 className="text-xl font-semibold">{section.title}</h3>
            <p className="mt-2 text-gray-600">{section.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

const sections = [
  { title: "Account Settings", description: "Manage your email, password, and security settings.", color: "#FF5733", icon: "🔐" },
  { title: "Payments & Billing", description: "View invoices, update payment details, and manage subscriptions.", color: "#33C3FF", icon: "💳" },
  { title: "Teams & Groups", description: "Create, manage, and collaborate with your team.", color: "#FFD700", icon: "👥" },
  { title: "Downloads & Sharing", description: "Save, share, and export your projects easily.", color: "#A833FF", icon: "📤" },
  { title: "Editing & Design", description: "Learn how to edit text, images, and layouts.", color: "#33FF77", icon: "🎨" },
  { title: "Troubleshooting", description: "Find solutions to common problems.", color: "#FF3380", icon: "🛠" },
];

export default KnowledgeBase;