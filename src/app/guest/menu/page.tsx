"use client";

import React, { useState } from 'react';

type MenuItem = {
  id: number;
  name: string;
  price: number;
  description: string;
  image: string;
};

type MenuCategory = {
  id: number;
  name: string;
  items: MenuItem[];
};

const menuData: MenuCategory[] = [
  {
    id: 1,
    name: "Món chính",
    items: [
      {
        id: 1,
        name: "Bún bò Huế",
        price: 45000,
        description: "Bún bò Huế truyền thống, đầy đủ các loại thịt và chả",
        image: "/images/bunbo.jpg"
      },
      {
        id: 2,
        name: "Phở bò",
        price: 40000,
        description: "Phở bò với nước dùng đậm đà, thịt bò tươi",
        image: "/images/phobo.jpg"
      },
      {
        id: 3,
        name: "Cơm tấm sườn",
        price: 35000,
        description: "Cơm tấm với sườn nướng, bì, chả, trứng",
        image: "/images/comtam.jpg"
      }
    ]
  },
  {
    id: 2,
    name: "Món khai vị",
    items: [
      {
        id: 1,
        name: "Gỏi cuốn tôm thịt",
        price: 15000,
        description: "Gỏi cuốn tươi với tôm, thịt heo và rau sống",
        image: "/images/goicuon.jpg"
      },
      {
        id: 2,
        name: "Chả giò",
        price: 20000,
        description: "Chả giò giòn rụm nhân thịt heo và nấm",
        image: "/images/chagio.jpg"
      }
    ]
  },
  {
    id: 3,
    name: "Món ăn kèm",
    items: [
      {
        id: 1,
        name: "Rau muống xào tỏi",
        price: 25000,
        description: "Rau muống xào với tỏi",
        image: "/images/raumuong.jpg"
      },
      {
        id: 2,
        name: "Cơm trắng",
        price: 10000,
        description: "Cơm trắng dẻo thơm",
        image: "/images/comtrang.jpg"
      }
    ]
  },
  {
    id: 4,
    name: "Món tráng miệng",
    items: [
      {
        id: 1,
        name: "Chè thái",
        price: 20000,
        description: "Chè thái thơm ngon với nhiều topping",
        image: "/images/chethai.jpg"
      },
      {
        id: 2,
        name: "Rau câu dừa",
        price: 15000,
        description: "Rau câu dừa mát lạnh",
        image: "/images/raucau.jpg"
      }
    ]
  },
  {
    id: 5,
    name: "Đồ uống",
    items: [
      {
        id: 1,
        name: "Trà đá",
        price: 5000,
        description: "Trà đá mát lạnh",
        image: "/images/trada.jpg"
      },
      {
        id: 2,
        name: "Cà phê sữa đá",
        price: 25000,
        description: "Cà phê sữa đá đậm đà",
        image: "/images/cafe.jpg"
      },
      {
        id: 3,
        name: "Nước chanh",
        price: 20000,
        description: "Nước chanh tươi mát",
        image: "/images/nuocchanh.jpg"
      }
    ]
  }
];

export default function MenuPage() {
  const [quantities, setQuantities] = useState<{ [key: string]: number }>({});

  const updateQuantity = (categoryId: number, itemId: number, value: number) => {
    const key = `${categoryId}-${itemId}`;
    setQuantities(prev => ({
      ...prev,
      [key]: Math.max(1, value) // Ensure quantity doesn't go below 1
    }));
  };

  const getQuantity = (categoryId: number, itemId: number): number => {
    const key = `${categoryId}-${itemId}`;
    return quantities[key] || 1;
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-center mb-8">Thực đơn</h1>
      
      <div className="space-y-12">
        {menuData.map((category) => (
          <div key={category.id} className="category">
            <h2 className="text-2xl font-semibold mb-6 border-b pb-2">
              {category.name}
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {category.items.map((item) => (
                <div key={item.id} className="bg-white rounded-lg shadow-md overflow-hidden">
                  <div className="h-48 relative">
                    <img
                      src={item.image}
                      alt={item.name}
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div className="p-4">
                    <div className="flex justify-between items-center mb-2">
                      <h3 className="text-lg font-semibold">{item.name}</h3>
                      <span className="text-green-600 font-bold">
                        {item.price.toLocaleString('vi-VN')}đ
                      </span>
                    </div>
                    <p className="text-gray-600 text-sm mb-4">{item.description}</p>
                    
                    <div className="flex items-center justify-between mt-4">
                      <div className="flex items-center gap-2">
                        <span className="text-sm">Số lượng</span>
                        <div className="flex items-center border rounded">
                          <button
                            className="px-2 py-1 border-r hover:bg-gray-100"
                            onClick={() => updateQuantity(category.id, item.id, getQuantity(category.id, item.id) - 1)}
                          >
                            -
                          </button>
                          <span className="px-4 py-1">
                            {getQuantity(category.id, item.id)}
                          </span>
                          <button
                            className="px-2 py-1 border-l hover:bg-gray-100"
                            onClick={() => updateQuantity(category.id, item.id, getQuantity(category.id, item.id) + 1)}
                          >
                            +
                          </button>
                        </div>
                      </div>
                      <button
                        className="bg-green-600 text-white px-4 py-2 rounded-full hover:bg-green-700 transition-colors"
                        onClick={() => {
                          // Handle order here
                          console.log(`Ordered ${getQuantity(category.id, item.id)} ${item.name}`);
                        }}
                      >
                        Đặt món
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}