"use client";

import React, { useState, useEffect } from 'react';

const saveToLocalStorage = (key: string, data: any) => {
    if (typeof window !== 'undefined') {
        localStorage.setItem(key, JSON.stringify(data));
    }
};

const loadFromLocalStorage = (key: string, defaultValue: any) => {
    if (typeof window !== 'undefined') {
        const stored = localStorage.getItem(key);
        return stored ? JSON.parse(stored) : defaultValue;
    }
    return defaultValue;
};

type Ingredient = {
    id: number;
    name: string;
    quantity: number;
    unit: string;
    status: 'sufficient' | 'low' | 'out_of_stock';
    warningLevel?: number;
    note?: string;
};


export default function IngredientsPage() {
    const [ingredients, setIngredients] = useState<Ingredient[]>(() =>
        loadFromLocalStorage('ingredients', [
            { id: 1, name: 'Thịt bò', quantity: 10000, unit: 'g', status: 'sufficient' },
            { id: 2, name: 'Bún', quantity: 5000, unit: 'g', status: 'sufficient' },
            { id: 3, name: 'Rau sống', quantity: 3000, unit: 'g', status: 'sufficient' },
        ])
    );

    const [isAddIngredientOpen, setIsAddIngredientOpen] = useState(false);
    const [newIngredient, setNewIngredient] = useState({
        name: '',
        quantity: '',
        unit: 'kg',
        warningLevel: '',
        note: ''
    });
    const [dialogMode, setDialogMode] = useState<'add' | 'edit'>('add');
    const [editingId, setEditingId] = useState<number | null>(null);
    const [isNoteDialogOpen, setIsNoteDialogOpen] = useState(false);
    const [selectedNote, setSelectedNote] = useState<{ id: number; note?: string }>({ id: 0, note: '' });

    useEffect(() => {
        saveToLocalStorage('ingredients', ingredients);
    }, [ingredients]);

    const getStatusColor = (status: Ingredient['status']) => {
        switch (status) {
            case 'sufficient':
                return 'bg-green-100 text-green-800';
            case 'low':
                return 'bg-yellow-100 text-yellow-800';
            case 'out_of_stock':
                return 'bg-red-100 text-red-800';
            default:
                return 'bg-gray-100 text-gray-800';
        }
    };

    const getStatusText = (status: Ingredient['status']) => {
        switch (status) {
            case 'sufficient':
                return 'Đủ hàng';
            case 'low':
                return 'Sắp hết';
            case 'out_of_stock':
                return 'Hết hàng';
            default:
                return status;
        }
    };

    const updateQuantity = (id: number, change: number) => {
        setIngredients(ingredients.map(ingredient => {
            if (ingredient.id === id) {
                const newQuantity = Math.max(0, ingredient.quantity + change);
                let newStatus: Ingredient['status'] = ingredient.status;

                if (newQuantity === 0) {
                    newStatus = 'out_of_stock';
                } else if (newQuantity <= 5) {
                    newStatus = 'low';
                } else {
                    newStatus = 'sufficient';
                }

                return {
                    ...ingredient,
                    quantity: newQuantity,
                    status: newStatus
                };
            }
            return ingredient;
        }));
    };

    const handleEditIngredient = (id: number) => {
        const ingredient = ingredients.find(i => i.id === id);
        if (ingredient) {
            setDialogMode('edit');
            setEditingId(id);
            setNewIngredient({
                name: ingredient.name,
                quantity: (ingredient.quantity / 1000).toString(), // Convert g to kg
                unit: 'kg',
                warningLevel: ingredient.warningLevel?.toString() || '',
                note: ingredient.note || ''
            });
            setIsAddIngredientOpen(true);
        }
    };

    const handleAddNote = (id: number) => {
        const ingredient = ingredients.find(i => i.id === id);
        if (ingredient) {
            setSelectedNote({
                id: ingredient.id,
                note: ingredient.note || ''
            });
            setIsNoteDialogOpen(true);
        }
    };

    // Add this function after other handlers
    const handleDeleteIngredient = (id: number) => {
        if (window.confirm('Bạn có chắc chắn muốn xóa nguyên liệu này?')) {
            setIngredients(ingredients.filter(ingredient => ingredient.id !== id));
        }
    };

    return (
        <div className="p-6">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold">Thêm nguyên liệu</h1>
                <button
                    onClick={() => setIsAddIngredientOpen(true)}
                    className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                >
                    Thêm nguyên liệu
                </button>
            </div>

            <div className="bg-gray-100 rounded-lg p-6">
                <table className="min-w-full">
                    <thead>
                        <tr className="border-b border-gray-200">
                            <th className="text-left pb-4 w-1/3">Tên nguyên liệu</th>
                            <th className="text-left pb-4 w-1/3">Số lượng</th>
                            <th className="text-right pb-4 w-1/3">Hành động</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                        {ingredients.map((ingredient) => (
                            <tr key={ingredient.id} className="hover:bg-gray-50">
                                <td className="py-4">{ingredient.name}</td>
                                <td className="py-4">
                                    {ingredient.quantity}g ({ingredient.quantity / 1000}kg)
                                </td>
                                <td className="py-4 text-right">
                                    <button
                                        onClick={() => handleEditIngredient(ingredient.id)}
                                        className="text-blue-600 hover:text-blue-800 mr-4"
                                    >
                                        Chỉnh sửa
                                    </button>
                                    {/* <button
                                        onClick={() => handleAddNote(ingredient.id)}
                                        className="text-gray-600 hover:text-gray-800 mr-4"
                                    >
                                        Xem ghi chú
                                    </button> */}
                                    <button
                                        onClick={() => handleDeleteIngredient(ingredient.id)}
                                        className="text-red-600 hover:text-red-800"
                                    >
                                        Xóa
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {isAddIngredientOpen && (
                <div className="fixed inset-0 flex items-center justify-center">
                    <div className="bg-white rounded-lg p-6 w-full max-w-md border-2 border-black">
                        <div className="flex justify-between items-center mb-4">
                            <h2 className="text-xl font-bold">
                                {dialogMode === 'add' ? 'Thêm nguyên liệu mới' : `Chỉnh sửa nguyên liệu - ${newIngredient.name}`}
                            </h2>
                            <button
                                onClick={() => {
                                    setIsAddIngredientOpen(false);
                                    setNewIngredient({
                                        name: '',
                                        quantity: '',
                                        unit: 'kg',
                                        warningLevel: '',
                                        note: ''
                                    });
                                    setEditingId(null);
                                    setDialogMode('add');
                                }}
                                className="text-gray-500 hover:text-gray-700"
                            >
                                ✕
                            </button>
                        </div>

                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Tên nguyên liệu
                                </label>
                                <input
                                    type="text"
                                    value={newIngredient.name}
                                    onChange={(e) => setNewIngredient({ ...newIngredient, name: e.target.value })}
                                    className="w-full border rounded-md px-3 py-2"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Số lượng
                                </label>
                                <div className="flex items-center gap-2">
                                    <input
                                        type="number"
                                        value={newIngredient.quantity}
                                        onChange={(e) => setNewIngredient({ ...newIngredient, quantity: e.target.value })}
                                        className="flex-1 border rounded-md px-3 py-2"
                                    />
                                    <span className="text-gray-700">kg</span>
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Mức cảnh báo sắp hết nguyên liệu:
                                </label>
                                <div className="flex items-center gap-2">
                                    <span className="text-gray-700">dưới</span>
                                    <input
                                        type="number"
                                        value={newIngredient.warningLevel}
                                        onChange={(e) => setNewIngredient({ ...newIngredient, warningLevel: e.target.value })}
                                        className="flex-1 border rounded-md px-3 py-2"
                                    />
                                    <span className="text-gray-700">kg</span>
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Ghi chú
                                </label>
                                <textarea
                                    value={newIngredient.note}
                                    onChange={(e) => setNewIngredient({ ...newIngredient, note: e.target.value })}
                                    className="w-full border rounded-md px-3 py-2 h-24 resize-none"
                                />
                            </div>
                        </div>

                        <div className="mt-6 flex justify-center">
                            <button
                                onClick={() => {
                                    if (dialogMode === 'add') {
                                        const newId = Math.max(...ingredients.map(i => i.id)) + 1;
                                        setIngredients([...ingredients, {
                                            id: newId,
                                            name: newIngredient.name,
                                            quantity: parseFloat(newIngredient.quantity) * 1000, // Convert kg to g
                                            unit: 'g',
                                            status: 'sufficient',
                                            warningLevel: parseFloat(newIngredient.warningLevel),
                                            note: newIngredient.note
                                        }]);
                                    } else if (editingId) {
                                        setIngredients(ingredients.map(ingredient =>
                                            ingredient.id === editingId ? {
                                                ...ingredient,
                                                name: newIngredient.name,
                                                quantity: parseFloat(newIngredient.quantity) * 1000, // Convert kg to g
                                                warningLevel: parseFloat(newIngredient.warningLevel),
                                                note: newIngredient.note
                                            } : ingredient
                                        ));
                                    }
                                    setIsAddIngredientOpen(false);
                                    setNewIngredient({
                                        name: '',
                                        quantity: '',
                                        unit: 'kg',
                                        warningLevel: '',
                                        note: ''
                                    });
                                    setEditingId(null);
                                    setDialogMode('add');
                                }}
                                className="px-8 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
                            >
                                {dialogMode === 'add' ? 'Thêm' : 'Sửa'}
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {isNoteDialogOpen && (
                <div className="fixed inset-0 flex items-center justify-center">
                    <div className="bg-white rounded-lg p-6 w-full max-w-md border-2 border-black">
                        <div className="flex justify-between items-center mb-4">
                            <h2 className="text-xl font-bold">
                                {ingredients.find(i => i.id === selectedNote.id)?.name} - Ghi chú
                            </h2>
                            <button
                                onClick={() => setIsNoteDialogOpen(false)}
                                className="text-gray-500 hover:text-gray-700"
                            >
                                ✕
                            </button>
                        </div>

                        <div className="space-y-4">
                            <textarea
                                value={selectedNote.note}
                                onChange={(e) => setSelectedNote({ ...selectedNote, note: e.target.value })}
                                className="w-full border rounded-md px-3 py-2 h-32 resize-none"
                                placeholder="Nhập ghi chú..."
                            />
                        </div>

                        <div className="mt-6 flex justify-end space-x-3">
                            <button
                                onClick={() => setIsNoteDialogOpen(false)}
                                className="px-4 py-2 border rounded-md hover:bg-gray-50"
                            >
                                Hủy
                            </button>
                            <button
                                onClick={() => {
                                    setIngredients(ingredients.map(ingredient =>
                                        ingredient.id === selectedNote.id
                                            ? { ...ingredient, note: selectedNote.note }
                                            : ingredient
                                    ));
                                    setIsNoteDialogOpen(false);
                                }}
                                className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
                            >
                                Lưu
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}