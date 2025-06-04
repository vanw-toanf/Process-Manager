def note_default_setting():
    """Ham nay mo ta default setting cua curses khi khong dung wrapper va dung wrapper"""
    print("Note:")
    print("- Mac dinh su dung cau hinh sau: ")
    print("  + curses.echo() : tat hien thi noi dung phim nhan")
    print("  + curses.nocbreak() : phai an enter de xac nhan noi dung")
    print("  + stdscr.keypad(False) : khong xu ly cac nut dac biet nhu ->,  <-, ^, v,...")
    print("      'stdscr' la ten duoc dat cho 1 doi tuong man hinh chinh cua curses")
    print("\n- O day se dung 1 ham goi la wrapper")
    print("   Ham nay co chuc nang thuc hien thay doi tren tu dong")
    print("** Neu khong dung wrapper, sau khi ket thuc chuong trinh ma quen thiet lap cau hinh cu")
    print("   Terminal se bi loi. Tham chi khi chuong trinh bi loi no cung khong in ra duoc loi.")
