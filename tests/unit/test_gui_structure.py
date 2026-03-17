"""
tests/unit/test_gui_structure.py — Smoke tests for GUI structure
"""

import tkinter as tk
import pytest
from src.gui_app import BrainNetGUI

class TestBrainNetGUI:
    def test_gui_init(self):
        root = tk.Tk()
        # Withdraw the root window to avoid a physical window appearing
        root.withdraw()
        
        try:
            gui = BrainNetGUI(root)
            assert gui.root == root
            assert gui.pipeline is not None
        finally:
            # We must destroy the root to clean up
            root.destroy()

    def test_metric_labels_initialization(self):
        root = tk.Tk()
        root.withdraw()
        try:
            gui = BrainNetGUI(root)
            # Verify metric stringvars are initialized
            assert isinstance(gui.m_p95, tk.StringVar)
            assert gui.m_p95.get() == "0.0 ms"
        finally:
            root.destroy()
