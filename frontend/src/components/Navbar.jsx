import { Link, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { logout } from "../features/auth/authSlice";

export default function Navbar() {
  const { user } = useSelector((state) => state.auth);
  const cartCount = useSelector((state) => state.cart.items.length);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleLogout = () => {
    dispatch(logout());
    navigate("/");
  };

  return (
    <header className="border-b-2 border-ink bg-paper sticky top-0 z-20">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="font-display text-2xl font-700 tracking-tight text-ink">
          Booked<span className="text-brass">.</span>
        </Link>

        <nav className="hidden md:flex items-center gap-6 text-sm font-medium">
          <Link to="/?section=store" className="hover:text-brass">Shop</Link>
          <Link to="/?section=library" className="hover:text-forest">Library</Link>
          {user && <Link to="/my-activity" className="hover:text-brass">My Activity</Link>}
          {user?.role === "admin" && <Link to="/admin" className="hover:text-brass">Admin</Link>}
        </nav>

        <div className="flex items-center gap-3">
          {user && (
            <Link to="/cart" className="relative text-sm font-medium hover:text-brass">
              Cart
              {cartCount > 0 && (
                <span className="absolute -top-2 -right-3 bg-burgundy text-paper text-[10px] rounded-full w-4 h-4 flex items-center justify-center">
                  {cartCount}
                </span>
              )}
            </Link>
          )}
          {user ? (
            <button onClick={handleLogout} className="text-sm border border-ink px-3 py-1 rounded-sm hover:bg-ink hover:text-paper transition">
              Log out
            </button>
          ) : (
            <>
              <Link to="/login" className="text-sm px-3 py-1 hover:text-brass">Log in</Link>
              <Link to="/register" className="text-sm bg-ink text-paper px-3 py-1 rounded-sm hover:bg-brass transition">
                Sign up
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
