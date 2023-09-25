// The standard interface.
interface IPool {
    struct TokenAmount {
        address token;
        uint amount;
    }

    /// @dev Returns the address of pool master.
    function master() external view returns (address);

    /// @dev Returns the vault.
    function vault() external view returns (address);

    // [Deprecated] This is the interface before the dynamic fees update.
    /// @dev Returns the pool type.
    function poolType() external view returns (uint16);

    /// @dev Returns the assets of the pool.
    function getAssets() external view returns (address[] memory assets);

    // [Deprecated] This is the interface before the dynamic fees update.
    /// @dev Returns the swap fee of the pool.
    // This function will forward calls to the pool master.
    // function getSwapFee() external view returns (uint24 swapFee);
    
     // [Recommended] This is the latest interface.
    /// @dev Returns the swap fee of the pool.
    /// This function will forward calls to the pool master.
    function getSwapFee(
        address sender, address tokenIn, address tokenOut, bytes calldata data
    ) external view returns (uint24 swapFee);

    /// @dev Returns the protocol fee of the pool.
    function getProtocolFee() external view returns (uint24 protocolFee);

    // [Deprecated] The old interface for Era testnet.
    /// @dev Mints liquidity.
    // The data for Classic and Stable Pool is as follows.
    // `address _to = abi.decode(_data, (address));`
    //function mint(bytes calldata data) external returns (uint liquidity);
    
    /// @dev Mints liquidity.
    function mint(
        bytes calldata data,
        address sender,
        address callback,
        bytes calldata callbackData
    ) external returns (uint liquidity);

    // [Deprecated] The old interface for Era testnet.
    /// @dev Burns liquidity.
    // The data for Classic and Stable Pool is as follows.
    // `(address _to, uint8 _withdrawMode) = abi.decode(_data, (address, uint8));`
    //function burn(bytes calldata data) external returns (TokenAmount[] memory amounts);

    /// @dev Burns liquidity.
    function burn(
        bytes calldata data,
        address sender,
        address callback,
        bytes calldata callbackData
    ) external returns (TokenAmount[] memory tokenAmounts);

    // [Deprecated] The old interface for Era testnet.
    /// @dev Burns liquidity with single output token.
    // The data for Classic and Stable Pool is as follows.
    // `(address _tokenOut, address _to, uint8 _withdrawMode) = abi.decode(_data, (address, address, uint8));`
    //function burnSingle(bytes calldata data) external returns (uint amountOut);

    /// @dev Burns liquidity with single output token.
    function burnSingle(
        bytes calldata data,
        address sender,
        address callback,
        bytes calldata callbackData
    ) external returns (TokenAmount memory tokenAmount);

    // [Deprecated] The old interface for Era testnet.
    /// @dev Swaps between tokens.
    // The data for Classic and Stable Pool is as follows.
    // `(address _tokenIn, address _to, uint8 _withdrawMode) = abi.decode(_data, (address, address, uint8));`
    //function swap(bytes calldata data) external returns (uint amountOut);

    /// @dev Swaps between tokens.
    function swap(
        bytes calldata data,
        address sender,
        address callback,
        bytes calldata callbackData
    ) external returns (TokenAmount memory tokenAmount);
}

// The base interface, with two tokens and Liquidity Pool (LP) token.
interface IBasePool is IPool, IERC20Permit2 {
    function token0() external view returns (address);
    function token1() external view returns (address);

    function reserve0() external view returns (uint);
    function reserve1() external view returns (uint);
    function invariantLast() external view returns (uint);

    function getReserves() external view returns (uint, uint);
    
    // [Deprecated] The old interface for Era testnet.
    //function getAmountOut(address tokenIn, uint amountIn) external view returns (uint amountOut);
    //function getAmountIn(address tokenOut, uint amountOut) external view returns (uint amountIn);

    function getAmountOut(address tokenIn, uint amountIn, address sender) external view returns (uint amountOut);
    function getAmountIn(address tokenOut, uint amountOut, address sender) external view returns (uint amountIn);

    event Mint(
        address indexed sender,
        uint amount0,
        uint amount1,
        uint liquidity,
        address indexed to
    );

    event Burn(
        address indexed sender,
        uint amount0,
        uint amount1,
        uint liquidity,
        address indexed to
    );

    event Swap(
        address indexed sender,
        uint amount0In,
        uint amount1In,
        uint amount0Out,
        uint amount1Out,
        address indexed to
    );

    event Sync(
        uint reserve0,
        uint reserve1
    );
}

// The Classic Pool.
interface IClassicPool is IBasePool {
}

// The Stable Pool with the additional multiplier for pool tokens.
interface IStablePool is IBasePool {
    function token0PrecisionMultiplier() external view returns (uint);
    function token1PrecisionMultiplier() external view returns (uint);
}

// The interface of callback (optional).
interface ICallback {

    struct BaseMintCallbackParams {
        address sender;
        address to;
        uint reserve0;
        uint reserve1;
        uint balance0;
        uint balance1;
        uint amount0;
        uint amount1;
        uint fee0;
        uint fee1;
        uint newInvariant;
        uint oldInvariant;
        uint totalSupply;
        uint liquidity;
        uint24 swapFee;
        bytes callbackData;
    }
    function syncSwapBaseMintCallback(BaseMintCallbackParams calldata params) external;

    struct BaseBurnCallbackParams {
        address sender;
        address to;
        uint balance0;
        uint balance1;
        uint liquidity;
        uint totalSupply;
        uint amount0;
        uint amount1;
        uint8 withdrawMode;
        bytes callbackData;
    }
    function syncSwapBaseBurnCallback(BaseBurnCallbackParams calldata params) external;

    struct BaseBurnSingleCallbackParams {
        address sender;
        address to;
        address tokenIn;
        address tokenOut;
        uint balance0;
        uint balance1;
        uint liquidity;
        uint totalSupply;
        uint amount0;
        uint amount1;
        uint amountOut;
        uint amountSwapped;
        uint feeIn;
        uint24 swapFee;
        uint8 withdrawMode;
        bytes callbackData;
    }
    function syncSwapBaseBurnSingleCallback(BaseBurnSingleCallbackParams calldata params) external;

    struct BaseSwapCallbackParams {
        address sender;
        address to;
        address tokenIn;
        address tokenOut;
        uint reserve0;
        uint reserve1;
        uint balance0;
        uint balance1;
        uint amountIn;
        uint amountOut;
        uint feeIn;
        uint24 swapFee;
        uint8 withdrawMode;
        bytes callbackData;
    }
    function syncSwapBaseSwapCallback(BaseSwapCallbackParams calldata params) external;
}
