import jwt from 'jsonwebtoken';

const secret = process.env.SECRET || 'secret';

const generateToken = (payload: any) => {
  return jwt.sign(payload, secret, {
    expiresIn: '1h',
    algorithm: 'HS512',
  });
}

export { generateToken };