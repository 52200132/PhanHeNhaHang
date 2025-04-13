"use client";

import React, { useState } from 'react';

type Dish = {
    id: number;
    name: string;
    category: string;
    price: number;
    priority: number;
    status: 'available' | 'unavailable';
};

type Ingredient = {
    name: string;
    quantity: string;
};

export default function DishesPage() {
    const [dishes, setDishes] = useState<Dish[]>([
        { id: 1, name: 'Bún bò Huế', category: 'Món chính', price: 50000, priority: 1, status: 'available' },
        { id: 2, name: 'Phở bò', category: 'Món chính', price: 45000, priority: 2, status: 'available' },
        { id: 3, name: 'Gỏi cuốn', category: 'Khai vị', price: 35000, priority: 3, status: 'unavailable' },
    ]);

    const [isAddDialogOpen, setIsAddDialogOpen] = useState(false);
    const [isIngredientDialogOpen, setIsIngredientDialogOpen] = useState(false);
    const [searchTerm, setSearchTerm] = useState('');
    const [availableIngredients] = useState([
        { id: 1, name: 'Thịt bò', unit: 'g' },
        { id: 2, name: 'Bún tươi', unit: 'g' },
        { id: 3, name: 'Chả lụa', unit: 'g' },
        { id: 4, name: 'Bắp bò', unit: 'g' },
        { id: 5, name: 'Giò heo', unit: 'g' },
    ]);
    const [newDish, setNewDish] = useState<Omit<Dish, 'id'>>({
        name: '',
        category: 'Món chính',
        price: 0,
        priority: 1,
        status: 'available'
    });
    const [ingredients, setIngredients] = useState<Ingredient[]>([{ name: '', quantity: '' }]);
    const [dialogMode, setDialogMode] = useState<'add' | 'edit'>('add');
    const [editingDish, setEditingDish] = useState<Dish | null>(null);

    const getStatusColor = (status: Dish['status']) => {
        switch (status) {
            case 'available':
                return 'bg-green-100 text-green-800';
            case 'unavailable':
                return 'bg-red-100 text-red-800';
            default:
                return 'bg-gray-100 text-gray-800';
        }
    };

    const getStatusText = (status: Dish['status']) => {
        switch (status) {
            case 'available':
                return 'Còn bán';
            case 'unavailable':
                return 'Hết món';
            default:
                return status;
        }
    };

    const toggleDishStatus = (dishId: number) => {
        setDishes(dishes.map(dish => {
            if (dish.id === dishId) {
                return {
                    ...dish,
                    status: dish.status === 'available' ? 'unavailable' : 'available'
                };
            }
            return dish;
        }));
    };

    const handleAddIngredient = () => {
        setIsIngredientDialogOpen(true);
    };

    const handleRemoveIngredient = (index: number) => {
        setIngredients(ingredients.filter((_, i) => i !== index));
    };

    const handleIngredientChange = (index: number, field: keyof Ingredient, value: string) => {
        const newIngredients = [...ingredients];
        newIngredients[index][field] = value;
        setIngredients(newIngredients);
    };

    const handleOpenAddDialog = () => {
        setDialogMode('add');
        setNewDish({ name: '', category: 'Món chính', price: 0, priority: 1, status: 'available' });
        setIsAddDialogOpen(true);
    };

    const handleOpenEditDialog = (dish: Dish) => {
        setDialogMode('edit');
        setEditingDish(dish);
        setNewDish({
            name: dish.name,
            category: dish.category,
            price: dish.price,
            priority: dish.priority,
            status: dish.status
        });
        setIngredients([
            { name: 'Bún tươi', quantity: '300g' },
            { name: 'Bắp bò', quantity: '100g' },
            { name: 'Chả lụa', quantity: '40g' }
        ]); // Giả lập dữ liệu nguyên liệu
        setIsAddDialogOpen(true);
    };

    const handleSubmit = () => {
        if (dialogMode === 'add') {
            const newId = Math.max(...dishes.map(d => d.id)) + 1;
            setDishes([...dishes, { ...newDish, id: newId }]);
        } else if (editingDish) {
            setDishes(dishes.map(dish =>
                dish.id === editingDish.id ? { ...editingDish, ...newDish } : dish
            ));
        }
        setIsAddDialogOpen(false);
        setNewDish({ name: '', category: 'Món chính', price: 0, priority: 1, status: 'available' });
        setIngredients([{ name: '', quantity: '' }]);
        setEditingDish(null);
    };

    const handleDelete = (dishId: number) => {
        if (window.confirm('Bạn có chắc chắn muốn xóa món ăn này không?')) {
            setDishes(dishes.filter(dish => dish.id !== dishId));
        }
    };

    return (
        <div className="p-6">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold">Danh sách món ăn</h1>
                <button
                    onClick={handleOpenAddDialog}
                    className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
                >
                    Thêm món
                </button>
            </div>

            {isAddDialogOpen && (
                <div className="fixed inset-0 flex items-center justify-center">
                    <div className="bg-white rounded-lg p-6 w-full max-w-md border-2 border-black">
                        <div className="flex justify-between items-center mb-4">
                            <h2 className="text-xl font-bold">
                                {dialogMode === 'add' ? 'Thêm món mới' : `Sửa món - ${editingDish?.name}`}
                            </h2>
                            <button
                                onClick={() => {
                                    setIsAddDialogOpen(false);
                                    setEditingDish(null);
                                }}
                                className="text-gray-500 hover:text-gray-700"
                            >
                                ✕
                            </button>
                        </div>

                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Tên món</label>
                                <input
                                    type="text"
                                    value={newDish.name}
                                    onChange={(e) => setNewDish({ ...newDish, name: e.target.value })}
                                    className="w-full border rounded-md px-3 py-2"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Phân loại</label>
                                <select
                                    value={newDish.category}
                                    onChange={(e) => setNewDish({ ...newDish, category: e.target.value })}
                                    className="w-full border rounded-md px-3 py-2"
                                >
                                    <option value="Món chính">Món chính</option>
                                    <option value="Khai vị">Khai vị</option>
                                    <option value="Tráng miệng">Tráng miệng</option>
                                </select>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Giá (VNĐ)</label>
                                <input
                                    type="number"
                                    value={newDish.price}
                                    onChange={(e) => setNewDish({ ...newDish, price: parseInt(e.target.value) })}
                                    className="w-full border rounded-md px-3 py-2"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Độ ưu tiên</label>
                                <input
                                    type="number"
                                    value={newDish.priority}
                                    onChange={(e) => setNewDish({ ...newDish, priority: parseInt(e.target.value) })}
                                    className="w-full border rounded-md px-3 py-2"
                                    min="1"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Trạng thái</label>
                                <select
                                    value={newDish.status}
                                    onChange={(e) => setNewDish({ ...newDish, status: e.target.value as 'available' | 'unavailable' })}
                                    className="w-full border rounded-md px-3 py-2"
                                >
                                    <option value="available">Còn bán</option>
                                    <option value="unavailable">Hết món</option>
                                </select>
                            </div>

                            <div>
                                <div className="flex justify-between items-center mb-2">
                                    <label className="block text-sm font-medium text-gray-700">Nguyên liệu chính</label>
                                    <button
                                        type="button"
                                        onClick={handleAddIngredient}
                                        className="text-sm text-blue-500 hover:text-blue-700"
                                    >
                                        + Thêm nguyên liệu
                                    </button>
                                </div>
                                {ingredients.map((ingredient, index) => (
                                    <div key={index} className="flex gap-2 mb-2">
                                        <div className="flex-1 border rounded-md px-3 py-2">
                                            {ingredient.name}
                                        </div>
                                        <div className="w-24 border rounded-md px-3 py-2">
                                            {ingredient.quantity}
                                        </div>
                                        <button
                                            type="button"
                                            onClick={() => handleRemoveIngredient(index)}
                                            className="text-red-500 hover:text-red-700 px-2"
                                        >
                                            ✕
                                        </button>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="mt-6 flex justify-end space-x-3">
                            <button
                                onClick={() => {
                                    setIsAddDialogOpen(false);
                                    setEditingDish(null);
                                }}
                                className="px-4 py-2 border rounded-md hover:bg-gray-50"
                            >
                                Hủy
                            </button>
                            <button
                                onClick={handleSubmit}
                                className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
                                disabled={!newDish.name || newDish.price <= 0}
                            >
                                {dialogMode === 'add' ? 'Thêm' : 'Sửa'}
                            </button>
                        </div>
                    </div>
                </div>
            )}

            <div className="bg-white rounded-lg shadow overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Món ăn
                            </th>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Giá
                            </th>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Độ ưu tiên
                            </th>
                            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Trạng thái
                            </th>
                            <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Hành động
                            </th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {dishes.map((dish) => (
                            <tr key={dish.id}>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <div className="text-sm font-medium text-gray-900">{dish.name}</div>
                                    <div className="text-sm text-gray-500">{dish.category}</div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {dish.price.toLocaleString('vi-VN')}đ
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {dish.priority}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(dish.status)}`}>
                                        {getStatusText(dish.status)}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                                    <button
                                        onClick={() => handleOpenEditDialog(dish)}
                                        className="text-indigo-600 hover:text-indigo-900"
                                    >
                                        Chỉnh sửa
                                    </button>
                                    <button
                                        onClick={() => handleDelete(dish.id)}
                                        className="text-red-600 hover:text-red-900"
                                    >
                                        Xóa
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {isIngredientDialogOpen && (
                <div className="fixed inset-0 flex items-center justify-center">
                    <div className="bg-white rounded-lg p-6 w-full max-w-md border border-black">
                        <div className="flex justify-between items-center mb-4">
                            <h2 className="text-xl font-bold">Thêm nguyên liệu chính</h2>
                            <button
                                onClick={() => setIsIngredientDialogOpen(false)}
                                className="text-gray-500 hover:text-gray-700"
                            >
                                ✕
                            </button>
                        </div>

                        <div className="mb-4">
                            <input
                                type="text"
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                placeholder="Tìm kiếm nguyên liệu..."
                                className="w-full border rounded-md px-3 py-2"
                            />
                        </div>

                        <div className="max-h-60 overflow-y-auto">
                            {availableIngredients
                                .filter(ing => ing.name.toLowerCase().includes(searchTerm.toLowerCase()))
                                .map(ingredient => (
                                    <div key={ingredient.id} className="flex items-center justify-between p-2 hover:bg-gray-50 rounded">
                                        <span>{ingredient.name}</span>
                                        <div className="flex items-center gap-2">
                                            <input
                                                type="number"
                                                placeholder="Số lượng"
                                                className="w-20 border rounded px-2 py-1"
                                                min="1"
                                            />
                                            <span className="text-gray-500">{ingredient.unit}</span>
                                            <button
                                                onClick={() => {
                                                    setIngredients([...ingredients, { name: ingredient.name, quantity: '100' }]);
                                                    setIsIngredientDialogOpen(false);
                                                }}
                                                className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
                                            >
                                                Thêm
                                            </button>
                                        </div>
                                    </div>
                                ))}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}